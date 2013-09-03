from hashlib import sha1
from numpy import all, array, uint8

def verify_mapping(items=None, bins=None, mapping=None):
    if items is None:
        return True
    if bins is None or mapping is None:
        return False
    allocs = [array([0] * len(bin_)) for bin_ in bins]
    for item, binidx in zip(items, mapping):
        if binidx is not None:
            allocs[binidx] += item
    if min((alloc <= bin_).all() for alloc, bin_ in zip(allocs, bins)):
        return True
    return False


def zero(*args, **kwargs):
    return 0


def negate_func(f, *args, **kwargs):
    return -f(*args, **kwargs)
