from itertools import islice, product
from numpy import array

def select_null(item=None, capacity=None):
    return None

def pack_first_fit_by_items(items=None, boxes=None, item_key=None, box_key=None):
    """ take items, map them to bins, return an array where each position
         represents the corresponding item and contains an index for the bin it
         should be packed in... """

    item_idxs = range(len(items))
    box_idxs = range(len(boxes))

    if item_key:
        item_idxs.sort(key=lambda i: item_key(items[i]))

    if box_key:
        box_idxs.sort(key=lambda b: box_key(boxes[b]))

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
    items=None, boxes=None, item_key=None, select_key=select_null):

    item_idxs = range(len(items))
    box_idxs = range(len(boxes))

    if item_key:
        item_idxs.sort(key=lambda i: item_key(items[i]))

    capacities = [array(b, copy=True) for b in boxes]

    mapping = [None] * len(items)

    for i in item_idxs:
        try:
            b = min((b for b in box_idxs if (items[i] <= capacities[b]).all()), 
                    key=lambda b: select_key(items[i], capacities[b]))
            mapping[i] = b
            capacities[b] -= items[i]
        except ValueError:
            return None

    return mapping

def pack_first_fit_by_boxes(
    items=None, boxes=None, item_key=None, box_key=None):

    item_idxs = range(len(items))
    box_idxs = range(len(boxes))

    if item_key:
        item_idxs.sort(key=lambda i: item_key(items[i]))

    if box_key:
        box_idxs.sort(key=lambda b: box_key(boxes[b]))

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
    items=None, boxes=None, box_key=None, select_key=select_null):

    item_idxs = set(range(len(items)))
    box_idxs = range(len(boxes))

    if box_key:
        box_idxs.sort(key=lambda b: box_key(boxes[b]))

    capacities = [array(b, copy=True) for b in boxes]

    mapping = [None] * len(items)

    for b in box_idxs:
        while True:
            try:
                i = min((i for i in item_idxs 
                         if (items[i] <= capacities[b]).all()),
                        key=lambda i: select_key(items[i], capacities[b]))
                mapping[i] = b
                capacities[b] -= items[i]
                item_idxs.remove(i) # fast because this is a set!
            except ValueError:
                break

    if len(item_idxs) > 0:
        return None

    return mapping

def pack_best_fit(items=None, boxes=None, select_key=select_null):

    item_idxs = set(range(len(items)))
    box_idxs = range(len(boxes))

    capacities = [array(b, copy=True) for b in boxes]

    mapping = [None] * len(items)

    while True:
        try:
            b, i = min(((b, i) for b, i in product(box_idxs, item_idxs) 
                        if (items[i] <= capacities[b]).all()),
                       key=lambda x: select_key(items[x[1]], capacities[x[0]]))
            mapping[i] = b
            capacities[b] -= items[i]
            item_idxs.remove(i) # fast because this is a set!
        except ValueError:
            break

    if len(item_idxs) > 0:
        return None

    return mapping
