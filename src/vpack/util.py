#!/usr/bin/env python

# here's something, any real reason to sort bins?
# maybe just always assume bin key also looks at item?
# okay, so for each way a sort and eval!

# item by item or bin by bin first fit
# best fit requires some kind of match quality function
# pp/cp basically works the same way, but the since we have to sort the items,
# maybe it doesn't make so much sense...why not just evaluate quality of match
# by maxdiff or something like that?

# yes it's called bin packing, but bin is a reserved word and box isn't

# assume numpy arrays

# also, l n norm...numpy.linalg.norm
# frobenius norm?

# FIXME: clean up variable names, too many i's and bin is a reserved word

# minor question: does first-fit offer real speed up over selection?

sorts = {
    "asum"       : sum,
    "amax"       : max,
    "amaxratio"  : (lambda v: float(max(v)) / min(v)), # could also do scaling?
    "amaxdiff"   : (lambda v: max(v) - min(v)),
    "none"       : None,
    "dsum"       : (lambda v: -sum(v)),
    "dmax"       : (lambda v: -max(v)),
    "dmaxtratio" : (lambda v: float(min(v)) / max(v)), # see above
    "dmaxdiff"   : (lambda v: min(v) - max(v))
}

# fixme don't actuall sort items...
def pack_first_fit_by_items(items=None, boxes=None, item_key=None, box_key=None):
    """ take items, map them to bins, return an array where each position
         represents the corresponding item and contains an index for the bin it
         should be packed in... """
    from numpy import array

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

def pack_first_fit_by_boxes(items=None, boxes=None, item_key=None, box_key=None):
    from numpy import array

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
        while i < len(item_idxs):
            try:
                j = next(j for j in range(i, len(item_idxs))
                         if (items[item_idxs[j]] <= capacities[b]).all())
                k = item_idxs[j]
                mapping[k] = b
                capacities[b] -= items[k]
                del item_idxs[j]
            except StopIteration:
                i += 1

    if len(item_idxs) > 0:
        return None

    return mapping

def match_null(item=None, capacity=None):
    return None

def compute_dimranks(box):
    dims = range(len(box))
    dims.sort(key=lambda x: (box[x], x))
    dimranks = [None] * len(box)
    for i in range(len(box)):
        dimranks[dims[i]] = i
    return dimranks

def compute_dimorder(item):
    dims = range(len(item))
    dims.sort(key=lambda x: (item[x], x))
    return dims
    
def match_dimorder(window, item, capacity):
    item_dims = compute_dimorder(item)
    box_dimranks = compute_dimranks(capacity)
    return [box_dimranks[dim] for dim in item_dims[:window]]

# FIXME: naming...
def match_dimset(window, item, capacity):
    item_dims = set(compute_dimorder(item)[:window])
    box_dimranks = set(compute_dimorder(capacity)[:window])
    return len(item_dims & box_dimranks)

def pack_select_by_items(items=None, boxes=None, item_key=None, match_key=match_null):
    from numpy import array

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

def pack_select_by_boxes(items=None, boxes=None, box_key=None, match_key=match_null):
    from numpy import array

    item_idxs = range(len(items))
    box_idxs = range(len(boxes))

    if box_key:
        box_idxs.sort(key=lambda b: box_key(boxes[b]))

    capacities = [array(b, copy=True) for b in boxes]

    mapping = [None] * len(items)

    for b in box_idxs:
        i = 0
        while i < len(item_idxs):
            try:
                j = min((j for j in range(i, len(item_idxs)) 
                        if (items[item_idxs[j]] <= capacities[b]).all()),
                        key=lambda k: match_key(items[item_idxs[k]], capacities[b]))
                k = item_idxs[j]
                mapping[k] = b
                capacities[b] -= items[k]
                del item_idxs[j]
            except ValueError:
                i += 1

    if len(item_idxs) > 0:
        return None

    return mapping
