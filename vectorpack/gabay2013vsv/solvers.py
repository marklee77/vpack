#!/usr/bin/env python3

from argparse import ArgumentParser

from yaml import load as yload, dump as ydump

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

try:
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Dumper

import time

from vsvbp.container import Item, Bin
import vsvbp.heuristics as heuristics
import vsvbp.measures as measures

class IndexedItem(Item):
    def __init__(self, requirements, index):
        self.index = index
        Item.__init__(self, requirements)

class IndexedBin(Bin):
    def __init__(self, capacities, index):
        self.index = index
        Bin.__init__(self, capacities)

def pack_vectors(problem, **kwargs):

    items = problem.get('items', None)
    bins = problem.get('bins', None)

    heuristic_name = kwargs.get('heuristic', None)
    item_measure_name = kwargs.get('item_measure', None)
    bin_measure_name = kwargs.get('bin_measure', None)
    single = kwargs.get('single', False)

    heuristic = getattr(heuristics, heuristic_name)
    item_measure = getattr(measures, item_measure_name)
    bin_measure = getattr(measures, bin_measure_name)

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
        'mapping' : mapping,
        'algo-runtime' : stop_time - start_time,
    }
