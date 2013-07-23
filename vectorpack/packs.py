from itertools import product
from functools import wraps
from numpy import array

from .util import zero

# FIXME: potential to speed up by bins / product using prefiltering...profile!

def _pack_by_items(
    items, item_idxs, bins, bin_idxs, select_key, mapping):

    for i in item_idxs:
        try:
            b = min((b for b in bin_idxs if (items[i] <= bins[b]).all()), 
                    key=lambda b: select_key(i, b))
            mapping[i] = b
            bins[b] -= items[i]
        except ValueError:
            return

def _pack_by_bins(
    items, item_idxs, bins, bin_idxs, select_key, mapping):

    for b in bin_idxs:
        while True:
            try:
                pi, i = min(((pi, i) for pi, i in enumerate(item_idxs) 
                             if (items[i] <= bins[b]).all()),
                            key=lambda x: select_key(x[1], b))
                mapping[i] = b
                bins[b] -= items[i]
                del item_idxs[pi]
            except ValueError:
                break

    if len(item_idxs) > 0:
        return


# FIXME: this could be smarter...for each item build a list of fitting bins...
# but needs an update every time...
def _pack_by_product(
    items, item_idxs, bins, bin_idxs, select_key, mapping):

    while True:
        try:
            pi, i, b = min(((pi, i, b) for pi, i, b in 
                            ((x[0], x[1], y) for x, y in 
                                product(enumerate(item_idxs), bin_idxs))
                            if (items[i] <= bins[b]).all()), 
                           key=lambda x: select_key(x[1], x[2]))
            mapping[i] = b
            bins[b] -= items[i]
            del item_idxs[pi]
        except ValueError:
            break

    if len(item_idxs) > 0:
        return

def _pack(items, bins, pack, item_key, bin_key, select_key):

    items_copy = None
    if items is not None:
        items_copy = [array(item, copy=True, dtype=int) for item in items]

    item_idxs = sorted(list(range(len(items_copy))),
                       key=lambda i: item_key(items_copy[i]))

    bins_copy = None
    if bins is not None:
        bins_copy = [array(bin_, copy=True, dtype=int) for bin_ in bins]

    bin_idxs = sorted(list(range(len(bins_copy))), 
                      key=lambda b: bin_key(bins_copy[b]))

    @wraps(select_key)
    def wrapped_select_key(i, b): 
        return select_key(items_copy[i], bins_copy[b])

    mapping = [None] * len(items_copy)

    pack(items_copy, item_idxs, bins_copy, bin_idxs, wrapped_select_key, 
         mapping)

    return mapping


def pack_by_items(
    items=None, bins=None, item_key=zero, bin_key=zero, select_key=zero):
    return _pack(items, bins, _pack_by_items, item_key, bin_key, select_key)


def pack_by_bins(
    items=None, bins=None, item_key=zero, bin_key=zero, select_key=zero):
    return _pack(items, bins, _pack_by_bins, item_key, bin_key, select_key)


def pack_by_product(
    items=None, bins=None, item_key=zero, bin_key=zero, select_key=zero):
    return _pack(items, bins, _pack_by_product, item_key, bin_key, select_key)

PACKS_BY_NAME = {
    "pack_by_items"   : pack_by_items,
    "pack_by_bins"    : pack_by_bins,
    "pack_by_product" : pack_by_product,
}

def list_packs():
    return PACKS_BY_NAME.keys()

def get_pack_by_name(name):
    return PACKS_BY_NAME[name]

