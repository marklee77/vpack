# FIXME: borked

def verify_mapping(items=None, bins=None, mapping=None, **kwargs):
    """ Verifies that mapping does not overfill any bins """
    if items is None:
        return True
    if bins is None or mapping is None:
        return False
    allocs = [tuple([0] * len(bin_)) for bin_ in bins]
    for item, binidx in zip(items, mapping):
        if binidx is not None:
            allocs[binidx] += item
    if min(all(alloc <= bin_) for alloc, bin_ in zip(allocs, bins)):
        return True
    return False
