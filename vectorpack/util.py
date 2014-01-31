from numpy import array

def verify_mapping(items=None, bins=None, mapping=None):
    """ Verifies that mapping does not overfill any bins """
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
    """ This function takes any arguments and always returns 0. """
    return 0


def negate_func(func):
    """ returns a function that returns the negation of f """
    return lambda *args, **kwargs: -func(*args, **kwargs)
