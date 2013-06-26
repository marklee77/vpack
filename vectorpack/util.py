from numpy import array

def verify_mapping(items=None, boxes=None, mapping=None):
    if boxes is None or mapping is None:
        return False
    if items is None:
        return True
    allocs = [array([0] * len(box)) for box in boxes]
    for item, boxidx in zip(items, mapping):
        allocs[boxidx] += item
    if min((alloc <= capacity).all() for alloc, capacity in zip(allocs, boxes)):
        return True
    return False
