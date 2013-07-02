from itertools import islice, product
from functools import partial
from numpy import array

from .sorts import null_sort_key
from .selects import null_select_key

# FIXME: rename capacities?
# FIXME: remove lambdas, replace with partials?

def pack_first_fit_by_items(
    items=None, boxes=None, item_key=null_sort_key, box_key=null_sort_key, 
    select_key=null_select_key):
    """ take items, map them to bins, return an array where each position
         represents the corresponding item and contains an index for the bin it
         should be packed in... """

    item_idxs = list(range(len(items)))
    box_idxs = list(range(len(boxes)))

    if item_key is not null_sort_key:
        item_idxs.sort(key=lambda i: (item_key(items[i]), i))

    if box_key is not null_sort_key:
        box_idxs.sort(key=lambda b: (box_key(boxes[b]), b))

    capacities = [array(b, copy=True) for b in boxes]

    mapping = [None] * len(items)

    for i in item_idxs:
        try:
            b = next(b for b in box_idxs if (items[i] <= capacities[b]).all())
            mapping[i] = b
            capacities[b] -= items[i]
        except StopIteration:
            return None

    return mapping

def pack_best_fit_by_items(
    items=None, boxes=None, item_key=null_sort_key, box_key=null_sort_key, 
    select_key=null_select_key):

    item_idxs = list(range(len(items)))
    box_idxs = list(range(len(boxes)))

    if item_key is not null_sort_key:
        item_idxs.sort(key=lambda i: (item_key(items[i]), i))

    capacities = [array(b, copy=True) for b in boxes]

    mapping = [None] * len(items)

    for i in item_idxs:
        try:
            b = min((b for b in box_idxs if (items[i] <= capacities[b]).all()), 
                    key=lambda b: (select_key(items[i], capacities[b]), 
                                   box_key(capacities[b]), 
                                   b))
            mapping[i] = b
            capacities[b] -= items[i]
        except ValueError:
            return None

    return mapping

def pack_first_fit_by_boxes(
    items=None, boxes=None, item_key=null_sort_key, box_key=null_sort_key, 
    select_key=null_select_key):

    item_idxs = list(range(len(items)))
    box_idxs = list(range(len(boxes)))

    if item_key is not null_sort_key:
        item_idxs.sort(key=lambda i: (item_key(items[i]), i))

    if box_key is not null_sort_key:
        box_idxs.sort(key=lambda b: (box_key(boxes[b]), b))

    capacities = [array(b, copy=True) for b in boxes]

    mapping = [None] * len(items)

    for b in box_idxs:
        i = 0
        while True:
            try:
                i, j = next(
                    (x + i, y) for x, y in enumerate(islice(item_idxs, i, None)) 
                    if (items[y] <= capacities[b]).all())
                mapping[j] = b
                capacities[b] -= items[j]
                del item_idxs[i] 
            except StopIteration:
                break

    if len(item_idxs) > 0:
        return None

    return mapping

def pack_best_fit_by_boxes(
    items=None, boxes=None, item_key=null_sort_key, box_key=null_sort_key,
    select_key=null_select_key):

    item_idxs = set(range(len(items)))
    box_idxs = list(range(len(boxes)))

    if box_key is not null_sort_key:
        box_idxs.sort(key=lambda b: (box_key(boxes[b]), b))

    capacities = [array(b, copy=True) for b in boxes]

    mapping = [None] * len(items)

    for b in box_idxs:
        while True:
            try:
                i = min((i for i in item_idxs 
                         if (items[i] <= capacities[b]).all()),
                        key=lambda i: (select_key(items[i], capacities[b]),
                                       item_key(items[i]), 
                                       i))
                mapping[i] = b
                capacities[b] -= items[i]
                item_idxs.remove(i) # fast because this is a set!
            except ValueError:
                break

    if len(item_idxs) > 0:
        return None

    return mapping

def pack_best_fit(
    items=None, boxes=None, item_key=null_sort_key, box_key=null_sort_key, 
    select_key=null_select_key):

    item_idxs = set(range(len(items)))
    box_idxs = list(range(len(boxes)))

    capacities = [array(b, copy=True) for b in boxes]

    mapping = [None] * len(items)

    while True:
        try:
            b, i = min(((b, i) for b, i in product(box_idxs, item_idxs) 
                        if (items[i] <= capacities[b]).all()),
                       key=lambda x: (select_key(items[x[1]], capacities[x[0]]),
                                      item_key(items[x[1]]),
                                      box_key(items[x[0]]),
                                      x))
            mapping[i] = b
            capacities[b] -= items[i]
            item_idxs.remove(i) # fast because this is a set!
        except ValueError:
            break

    if len(item_idxs) > 0:
        return None

    return mapping

PACKS_BY_NAME = {
    "first_fit_by_items" : pack_first_fit_by_items,
    "first_fit_by_boxes" : pack_first_fit_by_boxes,
    "best_fit_by_items"  : pack_best_fit_by_items,
    "best_fit_by_boxes"  : pack_best_fit_by_boxes,
    "best_fit"           : pack_best_fit,
}

def get_pack_names():
    return PACKS_BY_NAME.keys()

def get_pack_by_name(name):
    return PACKS_BY_NAME.get(name, None)
