#!/usr/bin/env python3

from argparse import ArgumentParser
from collections import Counter
from datetime import datetime
from functools import partial
from os.path import isfile
import time

from yaml import load as yload, dump as ydump

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

try:
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Dumper

from vectorpack.packs import get_pack_by_name
from vectorpack.sorts import parse_sort_cmdline
from vectorpack.selects import parse_select_cmdline
from vectorpack.util import verify_mapping, negate_func

def pack_vectors(**kwargs):

    pack = kwargs.get('pack', 'pack_by_bins')
    itemsort = kwargs.get('itemsort', 'none')
    binsort = kwargs.get('binsort', 'none')
    select = kwargs.get('select', 'none')
    split = max(1, kwargs.get('split', 1))
    problem = kwargs.get('problem', None)

    pack_func = get_pack_by_name(pack)
    item_key = parse_sort_cmdline(itemsort)
    bin_key = parse_sort_cmdline(binsort)
    select_key = parse_select_cmdline(select)

    items = problem.get('items', None)
    bins = problem.get('bins', None)

    start_time = time.process_time()
    mapping = pack_func(items=items, bins=bins, 
                        item_key=item_key, bin_key=bin_key, 
                        select_key=select_key, 
                        split=split)
    stop_time = time.process_time()

    return {
        'solver-githash' : '__GITHASH__',
        'problem-argshash' : problem.get('argshash', None),
        'pack' : pack,
        'itemsort' : itemsort,
        'binsort' : binsort,
        'select' : select,
        'split' : split,
        'datetime' : datetime.now(),
        'mapping' : mapping,
        'failcount' : mapping.count(None),
        'bincount' : len(Counter(mapping)),
        'verified' : verify_mapping(items=items, bins=bins, mapping=mapping),
        'runtime' : stop_time - start_time,
    }

def pack_vectors_gabay2013vsv(**kwargs):
    from vsvbp.container import Item, Bin

    class IndexedItem(Item):
        def __init__(self, requirements, index):
            self.index = index
            Item.__init__(self, requirements)

    class IndexedBin(Bin):
        def __init__(self, capacities, index):
            self.index = index
            Bin.__init__(self, capacities)

    heuristic = kwargs.get('heuristic', None)
    item_measure = kwargs.get('item_measure', None)
    bin_measure = kwargs.get('bin_measure', None)
    single = kwargs.get('single', False)
    problem = kwargs.get('problem', None)

    items = problem.get('items', None)
    bins = problem.get('bins', None)

    item_objects = [IndexedItem(r, i) for i, r in enumerate(items)]
    bin_objects = [IndexedBin(c, i) for i, c in enumerate(bins)]

    # FIXME: single for balance?
    start_time = time.process_time()
    failed = heuristic(item_objects, bin_objects, item_measure, bin_measure)
    stop_time = time.process_time()

    mapping = [None] * len(items)

    # FIXME: probably a more pythonic way to do this...
    for bin_object in bin_objects:
        for item_object in bin_object.items:
            mapping[item_object.index] = bin_object.index

    # FIXME: method names?
    return {
        'solver-githash' : '__GITHASH__',
        'problem-argshash' : problem.get('argshash', None),
        'algorithm' : { 'type' : 'heuristic', 
                        'family' : 'gabay2013vsv', 
                        'params' : None },
        'datetime' : datetime.now(),
        'mapping' : mapping,
        'failcount' : mapping.count(None),
        'bincount' : len(Counter(mapping)),
        'verified' : verify_mapping(items=items, bins=bins, mapping=mapping),
        'runtime' : stop_time - start_time,
    }

def pack_vectors_openopt(**kwargs):
    from openopt import BPP

    solver = kwargs.get('solver', 'glpk')
    iprint = kwargs.get('iprint', -1)

    problem = kwargs.get('problem', None)

    items = problem.get('items', None)
    bins = problem.get('bins', None)

    # FIXME: smarter handling of items of the same type...
    openopt_items = [dict([('name', i), ('n', 1)] + 
                          [('d{:d}'.format(d), r) for d, r in enumerate(item)])
                     for i, item in enumerate(items)]

    bin_set = set(tuple(bin_) for bin_ in bins)
    if len(bin_set) != 1:
        raise Exception('openopt can only work with homogeneous bins')

    openopt_bins = dict(
        [('d{:d}'.format(d), c) for d, c in enumerate(bins[0])] +
        [('n', len(bins))]
    )

    openopt_prob = BPP(openopt_items, openopt_bins)

    # FIXME: single for balance?
    start_time = time.process_time()
    openopt_result = openopt_prob.solve(solver, iprint=iprint)
    stop_time = time.process_time()

    mapping = [None] * len(items)
    for b, bin_contents in enumerate(openopt_result.xf):
        for i, count in bin_contents.items():
            mapping[i] = b

    # FIXME: method names?
    return {
        'solver-githash' : '__GITHASH__',
        'problem-argshash' : problem.get('argshash', None),
        'algorithm' : { 'type' : 'exact', 
                        'family' : 'openopt', 
                        'solver' : solver,
                        'iprint' : iprint },
        'datetime' : datetime.now(),
        'mapping' : mapping,
        'failcount' : mapping.count(None),
        'bincount' : len(Counter(mapping)),
        'verified' : verify_mapping(items=items, bins=bins, mapping=mapping),
        'runtime' : stop_time - start_time,
    }

def pack_vectors_vpsolver(**kwargs):
    from pyvpsolver import solve_mvbp

    solver = kwargs.get('solver', 'glpk')
    verbose = kwargs.get('verbose', False)

    problem = kwargs.get('problem', None)

    items = problem.get('items', None)
    bins = problem.get('bins', None)

    # FIXME: smarter handling of items of the same type...
    # brandao can only handle int contents...
    vpsolver_items = [[[1000 * int(r) for r in item]] for item in items]

    bin_set = set(tuple(bin_) for bin_ in bins)
    if len(bin_set) != 1:
        # FIXME: well, for now...
        raise Exception('vpsolver can only work with homogeneous bins')

    vpsolver_bins = [tuple(1000 * int(c) for c in bins[0])]

    b = [1] * len(items)
    cost = [1]

    script = "vpsolver_" + solver + ".sh"

    # FIXME: single for balance?
    start_time = time.process_time()
    _, sol = solve_mvbp(vpsolver_bins, vpsolver_items, b, cost, 
                        verbose=verbose, script=script)
    stop_time = time.process_time()

    mapping = [None] * len(items)
    for b, (_, bin_contents) in enumerate(sol[0]):
        for i, _ in bin_contents:
            mapping[i] = b

    # FIXME: method names?
    return {
        'solver-githash' : '__GITHASH__',
        'problem-argshash' : problem.get('argshash', None),
        'algorithm' : { 'type' : 'exact', 
                        'family' : 'brandao2013vsv', 
                        'solver' : solver,
                        'verbose' : verbose },
        'datetime' : datetime.now(),
        'mapping' : mapping,
        'failcount' : mapping.count(None),
        'bincount' : len(Counter(mapping)),
        'verified' : verify_mapping(items=items, bins=bins, mapping=mapping),
        'runtime' : stop_time - start_time,
    }

def main(argv=None):

    parser = ArgumentParser(description="Solve a vector packing problem.")
    parser.add_argument('-i', '--input', help='input file')
    parser.add_argument('-o', '--output', default='-', help='output file')
    parser.add_argument('-P', '--pack', default='pack_by_bins', 
                        help='packing algorithm')
    parser.add_argument('-I', '--itemsort', default='none', 
                        help='item sorting algorithm')
    parser.add_argument('-B', '--binsort', default='none', 
                        help='bin sorting algorithm')
    parser.add_argument('-S', '--select', default='none', 
                        help='pairwise selection algorithm')
    parser.add_argument('-s', '--split', default=1, type=int,
                        help='split the problem')

    args = parser.parse_args()

    args.problem = {}
    if isfile(args.input):
        args.problem = yload(open(args.input, 'r'), Loader=Loader)
    else:
        raise SystemExit("error: can't find file %s" % args.input)

    solution = pack_vectors(**args.__dict__)

    # FIXME: hacky
    mclient = None
    mcoll = None
    if args.output.startswith("mongodb://"):
        try:
            dbinfo = uri_parser.parse_uri(args.output)
            host, port = dbinfo['nodelist'][0]
            db, collection = dbinfo['database'].split('/')
            username = dbinfo['username']
            password = dbinfo['password']
            connect_url = host + ':' + str(port)
            if username is not None and password is not None:
                connect_url = username + ':' + password + '@' + connect_url
            connect_url = 'mongodb://' + connect_url
        except (AttributeError, ValueError):
            raise SystemExit('Required mongodb output url format is ' 
                '"mongodb://[user:pass@]host[:port]/database/collection"')
        mclient = MongoClient(connect_url)
        mcoll = mclient[db][collection]
        if mcoll.find_one(solution) is not None:
            raise SystemExit('Solution To This Problem Already Exists!')

    if mcoll is not None and mclient is not None:
        mcoll.insert(solution)
        mclient.close()
    else:
        print(ydump(solution, Dumper=Dumper))

if __name__ == "__main__":
    main() 
