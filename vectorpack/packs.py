from itertools import islice, product
from functools import wraps
from numpy import array

from .util import zero

def _pack_first_fit_by_items(
    items, item_idxs, bins, bin_idxs, select_key, mapping):

    for i in item_idxs:
        try:
            b = next(b for b in bin_idxs if (items[i] <= bins[b]).all())
            mapping[i] = b
            bins[b] -= items[i]
        except StopIteration:
            return None

    return mapping


def _pack_best_fit_by_items(
    items, item_idxs, bins, bin_idxs, select_key, mapping):

    for i in item_idxs:
        try:
            b = min((b for b in bin_idxs if (items[i] <= bins[b]).all()), 
                    key=select_key)
            mapping[i] = b
            bins[b] -= items[i]
        except ValueError:
            return None

    return mapping

def _pack_first_fit_by_bins(
    items, item_idxs, bins, bin_idxs, select_key, mapping):

    for b in bin_idxs:
        i = 0
        while True:
            try:
                i, j = next(
                    (x + i, y) for x, y in enumerate(islice(item_idxs, i, None)) 
                    if (items[y] <= bins[b]).all())
                mapping[j] = b
                bins[b] -= items[j]
                del item_idxs[i] 
            except StopIteration:
                break

    if len(item_idxs) > 0:
        return None

    return mapping


def _pack_best_fit_by_bins(
    items, item_idxs, bins, bin_idxs, select_key, mapping):

    for b in bin_idxs:
        while True:
            try:
                i = min((i for i in item_idxs if (items[i] <= bins[b]).all()),
                        key=select_key)
                mapping[i] = b
                bins[b] -= items[i]
                item_idxs.remove(i) # FIXME: fast because this is a set!
            except ValueError:
                break

    if len(item_idxs) > 0:
        return None

    return mapping


def _pack_best_fit(
    items, item_idxs, bins, bin_idxs, select_key, mapping):

    while True:
        try:
            b, i = min(((b, i) for b, i in product(bin_idxs, item_idxs) 
                       if (items[i] <= bins[b]).all()), key=select_key)
            mapping[i] = b
            bins[b] -= items[i]
            item_idxs.remove(i) # FIXME: fast because this is a set!
        except ValueError:
            break

    if len(item_idxs) > 0:
        return None

    return mapping

def wrap_sort_key_func(f, vlist):
    @wraps(f)
    def g(idx): return f(vlist[idx])
    return g


def wrap_select_key_func(f, items, bins):
    @wraps(f)
    def g(i, b): return f(items[i], bins[b])
    return g

def pack_first_fit_by_items(
    items=None, bins=None, item_key=zero, bin_key=zero, select_key=zero):
        newbins = None
        if bins is not None:
            newbins = [array(b, copy=True) for b in bins]
        new_item_key = wrap_sort_key_func(item_key, items)
        new_bin_key = wrap_sort_key_func(bin_key, newbins)
        new_select_key = wrap_select_key_func(select_key, items, bins)
        item_idxs = sorted(list(range(len(items))), key=new_item_key)
        bin_idxs = sorted(list(range(len(bins))), key=new_bin_key)
        mapping = [None] * len(items)
    return _pack_first_fit_by_items(items=items, bins=newbins, 
                                    item_key=new_item_key, bin_key=new_bin_key, 
                                    select_key=new_select_key)



def pack_best_fit_by_items(
    items=None, bins=None, item_key=none_sort_key, bin_key=none_sort_key, 
    select_key=null_select_key):
        newbins = None
        if bins is not None:
            newbins = [array(b, copy=True) for b in bins]
        new_item_key = wrap_sort_key_func(item_key, items)
        new_bin_key = wrap_sort_key_func(bin_key, newbins)
        new_select_key = wrap_select_key_func(select_key, items, bins)
    return _pack_best_fit_by_items(items=items, bins=newbins, 
                                    item_key=new_item_key, bin_key=new_bin_key, 
                                    select_key=new_select_key)




def pack_first_fit_by_bins(
    items=None, bins=None, item_key=none_sort_key, bin_key=none_sort_key, 
    select_key=null_select_key):
        newbins = None
        if bins is not None:
            newbins = [array(b, copy=True) for b in bins]
        new_item_key = wrap_sort_key_func(item_key, items)
        new_bin_key = wrap_sort_key_func(bin_key, newbins)
        new_select_key = wrap_select_key_func(select_key, items, bins)
    return _pack_best_fit_by_items(items=items, bins=newbins, 
                                    item_key=new_item_key, bin_key=new_bin_key, 
                                    select_key=new_select_key)




PACKS_BY_NAME = {
    "first_fit_by_items" : pack_first_fit_by_items,
    "first_fit_by_bins" : pack_first_fit_by_bins,
    "best_fit_by_items"  : pack_best_fit_by_items,
    "best_fit_by_bins"  : pack_best_fit_by_bins,
    "best_fit"           : pack_best_fit,
}

def get_pack_names():
    return PACKS_BY_NAME.keys()

def get_pack_by_name(name):
    return PACKS_BY_NAME.get(name, None)
