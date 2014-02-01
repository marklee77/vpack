from sys import maxsize as maxint

from numpy import array
from numpy.linalg import norm as lnorm

def imaxratio(v):
    maxval = max(v)
    minval = min(v)
    if minval == 0.0:
        return maxint
    return 1000 * maxval // minval

def _pack_by_bins(items, item_idxs, bins, bin_idxs, mapping):

    for b in bin_idxs:
        while True:
            try:
                pi, i = min(((pi, i) for pi, i in enumerate(item_idxs) 
                             if (items[i] <= bins[b]).all()),
                            key=lambda x: select_key(b - x[1]))
                mapping[i] = b
                bins[b] -= items[i]
                del item_idxs[pi]
            except ValueError:
                break

    if len(item_idxs) > 0:
        return


def pack_optimized(items=None, bins=None, split=1):

    items_copy = None
    if items is not None:
        items_copy = [array(item, copy=True, dtype=int) for item in items]

    num_items = len(items_copy)
    item_idxs = list(range(num_items))

    bins_copy = None
    if bins is not None:
        bins_copy = [array(bin_, copy=True, dtype=int) for bin_ in bins]

    num_bins = len(bins_copy)
    bin_idxs = list(range(num_bins))

    mapping = [None] * len(items_copy)

    items_sublist_size, items_remaining = divmod(num_items, split)
    items_sublist_ubs = list(accumulate(
        [items_sublist_size] * (split - items_remaining) + 
        [items_sublist_size+1] * items_remaining))
        
    bins_sublist_size, bins_remaining = divmod(num_bins, split)
    bins_sublist_ubs = list(accumulate(
        [bins_sublist_size] * (split - bins_remaining) + 
        [bins_sublist_size+1] * bins_remaining))
    
    bounds = list(zip([0] + items_sublist_ubs[:-1], items_sublist_ubs,
                      [0] + bins_sublist_ubs[:-1], bins_sublist_ubs))

    for item_idxs_lb, item_idxs_ub, bin_idxs_lb, bin_idxs_ub in bounds:
        item_idxs_sublist = item_idxs[item_idxs_lb:item_idxs_ub]
        item_idxs_sublist.sort(key=lambda i: item_key(items_copy[i]))
        bin_idxs_sublist = bin_idxs[bin_idxs_lb:bin_idxs_ub]
        bin_idxs_sublist.sort(key=lambda b: bin_key(bins_copy[b]))
        pack(items_copy, item_idxs_sublist, bins_copy, bin_idxs_sublist, 
             wrapped_select_key, mapping)

    return mapping

