#!/usr/bin/env python3
# FIXME: own custom classes or numpy arrays?

from argparse import ArgumentParser
from collections import Counter
from datetime import datetime
from functools import partial
from os.path import isfile
from random import sample
from sys import stdin, stdout
import time

from numpy import array
from pymongo import MongoClient, uri_parser
from yaml import load as yload, dump as ydump

try:
    from yaml import CLoader as YLoader
except ImportError:
    from yaml import Loader as YLoader

try:
    from yaml import CDumper as YDumper
except ImportError:
    from yaml import YDumper

from vectorpack.packs import get_pack_by_name
from vectorpack.sorts import get_sort_key_by_name
from vectorpack.selects import get_select_by_name
from vectorpack.util import verify_mapping, negate_func, zero

#import cProfile

def parse_sort_cmdline(sortcmd):
    args = sortcmd.split(":")

    arg = args.pop(0)
    desc = False
    if arg in [ "a", "d" ]:
        if arg is "d":
            desc = True
        arg = args.pop(0)

    sort_key = get_sort_key_by_name(arg)

    kwargs = {}
    if args:
        kwargs.update(yload("\n".join(arg.replace('=', ': ') for arg in args)))

    if desc:
        return partial(negate_func, sort_key, **kwargs)

    if kwargs:
        return partial(sort_key, **kwargs)

    return sort_key


def parse_select_cmdline(sortcmd):
    args = sortcmd.split(":")

    arg = args.pop(0)
    desc = False
    if arg in [ "a", "d" ]:
        if arg is "d":
            desc = True
        arg = args.pop(0)

    select_key = get_select_by_name(arg)

    kwargs = {}
    if args:
        kwargs.update(yload("\n".join(arg.replace('=', ': ') for arg in args)))

    if desc:
        return partial(negate_func, select_key, **kwargs)

    if kwargs:
        return partial(select_key, **kwargs)

    return select_key


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

    problem = {}
    if isfile(args.input):
        problem = yload(open(args.input, 'r'), Loader=YLoader)
    else:
        raise SystemExit("error: can't find file %s" % args.input)

    items = problem.get('items', None)
    bins = problem.get('bins', None)
    pack = get_pack_by_name(args.pack)
    item_key = parse_sort_cmdline(args.itemsort)
    bin_key = parse_sort_cmdline(args.binsort)
    select_key = parse_select_cmdline(args.select)
    split = max(1, args.split)

    solution = {
        'problem-argshash' : problem.get('argshash', None),
        'pack' : args.pack,
        'itemsort' : args.itemsort,
        'binsort' : args.binsort,
        'select' : args.select,
        'split' : split,
    }

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

    mapping = []

    #pr = cProfile.Profile()
    #pr.enable()
    start_time = time.process_time()
    mapping = pack(items=items, bins=bins, 
                   item_key=item_key, bin_key=bin_key, 
                   select_key=select_key, split=split)
    stop_time = time.process_time()
    #pr.disable()
    #pr.create_stats()
    #pr.dump_stats('pack-vectors.profile')

    solution.update({
        'solver-githash' : 'GITHASH',
        'datetime' : datetime.now(),
        'mapping' : mapping,
        'failcount' : mapping.count(None),
        'bincount' : len(Counter(mapping)),
        'verified' : verify_mapping(items=items, bins=bins, mapping=mapping),
        'runtime' : stop_time - start_time,
    })

    if mcoll is not None and mclient is not None:
        mcoll.insert(solution)
        mclient.close()
    else:
        print(ydump(solution, Dumper=YDumper))

if __name__ == "__main__":
    main() 
