#!/usr/bin/env python
from itertools import islice, product
from numpy import array
from numpy.linalg import norm

# yes it's called bin packing, but bin is a reserved word and box isn't

# item by item or bin by bin first fit
# best fit requires some kind of match quality function
# pp/cp basically works the same way, but the since we have to sort the items,
# maybe it doesn't make so much sense...why not just evaluate quality of match
# by maxdiff or something like that?

# assume numpy arrays

# also, l n norm...numpy.linalg.norm
# frobenius norm?

# minor question: does first-fit offer real speed up over selection?

# norms based on numpy.linalg.norm...
# something like arctan dist from 45, but multidimensional

# TODO:
#   * documentation
#   * problem instance generator & test runner
#   * unit testing
#   * initial benchmarking
#   * profiling, memcache, cython benefits
#   * develop portfolio
#       - multithreaded with abort on find...

# FIXME: GLOBAL solution quality metrics...


sorts = {
    "asum"       : sum,
    "al2"        : (lambda v: norm(v, ord=2)),
    "amax"       : max,
    "amaxratio"  : (lambda v: float(max(v)) / min(v)), # could also do scaling?
    "amaxdiff"   : (lambda v: max(v) - min(v)),
    "none"       : None,
    "dsum"       : (lambda v: -sum(v)),
    "dl2"        : (lambda v: -norm(v, ord=2)),
    "dmax"       : (lambda v: -max(v)),
    "dmaxtratio" : (lambda v: float(min(v)) / max(v)), # see above
    "dmaxdiff"   : (lambda v: min(v) - max(v))
}

# look up min cover algo...

# matches
# dim matching for pp/cp
# same as sorts on cap - item
#  * pick smallest sum is best fit
#  * pick smallest maxration/maxdiff should be close to pp

# FIXME: should match functions get global state info?

# FIXME: memory cache? need to profile...
def compute_dimorder(vector):
    dims = range(len(vector))
    dims.sort(key=lambda x: (vector[x], x))
    return dims
    
def compute_dimranks(vector):
    dims = compute_dimorder(vector)
    dimranks = [None] * len(vector)
    for i in range(len(dims)):
        dimranks[dims[i]] = i
    return dimranks

def match_dimorder(window, item, capacity):
    dims = compute_dimorder(item)
    dimranks = compute_dimranks(capacity)
    return [dimranks[dim] for dim in dims[:window]]

# FIXME: naming...
def match_dimset(window, item, capacity):
    item_dims = set(compute_dimorder(item)[:window])
    box_dimranks = set(compute_dimorder(capacity)[:window])
    return len(item_dims & box_dimranks)

def match_null(item=None, capacity=None):
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

def pack_best_fit_by_items(items=None, boxes=None, item_key=None, match_key=match_null):

    item_idxs = range(len(items))
    box_idxs = range(len(boxes))

    if item_key:
        item_idxs.sort(key=lambda i: item_key(items[i]))

    capacities = [array(b, copy=True) for b in boxes]

    mapping = [None] * len(items)

    for i in item_idxs:
        try:
            b = min((b for b in box_idxs if (items[i] <= capacities[b]).all()), 
                    key=lambda b: match_key(items[i], capacities[b]))
            mapping[i] = b
            capacities[b] -= items[i]
        except ValueError:
            return None

    return mapping

def pack_first_fit_by_boxes(items=None, boxes=None, item_key=None, box_key=None):

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
                i, j = next((x + i, y) for x, y in enumerate(islice(item_idxs, i, None))
                         if (items[y] <= capacities[b]).all())
                mapping[j] = b
                capacities[b] -= items[j]
                del item_idxs[i] 
            except StopIteration:
                break

    if len(item_idxs) > 0:
        return None

    return mapping

def pack_best_fit_by_boxes(items=None, boxes=None, box_key=None, match_key=match_null):

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
                        key=lambda i: match_key(items[i], capacities[b]))
                mapping[i] = b
                capacities[b] -= items[i]
                item_idxs.remove(i) # fast because this is a set!
            except ValueError:
                break

    if len(item_idxs) > 0:
        return None

    return mapping

# repeatedly go through and pick the best match...largest complexity...
# need to recalculate matchings with items for last selected bin...
def pack_best_fit(items=None, boxes=None, box_key=None, match_key=match_null):

    item_idxs = set(range(len(items)))
    box_idxs = range(len(boxes))

    capacities = [array(b, copy=True) for b in boxes]

    mapping = [None] * len(items)

    while True:
        try:
            b, i = min(((b, i) for b, i in product(box_idxs, item_idxs) 
                        if (items[i] <= capacities[b]).all()),
                       key=lambda x: match_key(items[x[1]], capacities[x[0]]))
            mapping[i] = b
            capacities[b] -= items[i]
            item_idxs.remove(i) # fast because this is a set!
        except ValueError:
            break

    if len(item_idxs) > 0:
        return None

    return mapping
