"""
This code is part of the XXX.

Copyright (C) 2013, Mark Stillwell <marklee@fortawesome.org>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from functools import wraps
from itertools import accumulate, product

import numpy as np

from .util import zero


# FIXME: prefiltering?
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


# FIXME: prefiltering?
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


# FIXME: put in util?
def _split_problem(item_idxs, bin_idxs, split):

    items_sublist_size, items_remaining = divmod(len(item_idxs), split)
    items_sublist_ubs = list(accumulate(
        [items_sublist_size] * (split - items_remaining) + 
        [items_sublist_size+1] * items_remaining))
        
    item_idxs_sublists = [item_idxs[lb:ub] for lb, ub in 
                          zip([0] + items_sublist_ubs[:-1], items_sublist_ubs)]

    bins_sublist_size, bins_remaining = divmod(len(bin_idxs), split)
    bins_sublist_ubs = list(accumulate(
        [bins_sublist_size] * (split - bins_remaining) + 
        [bins_sublist_size+1] * bins_remaining))
    
    bin_idxs_sublists = [bin_idxs[lb:ub] for lb, ub in
                         zip([0] + bins_sublist_ubs[:-1], bins_sublist_ubs)]

    return zip(item_idxs_sublists, bin_idxs_sublists)

def _pack(items, bins,
          pack, select_key, item_key, bin_key, split, 
          mapping):

    items_copy = None
    if items is not None:
        items_copy = [np.array(item, copy=True, dtype=int) for item in items]

    num_items = len(items_copy)
    item_idxs = list(range(num_items))

    bins_copy = None
    if bins is not None:
        bins_copy = [np.array(bin_, copy=True, dtype=int) for bin_ in bins]

    num_bins = len(bins_copy)
    bin_idxs = list(range(num_bins))

    @wraps(select_key)
    def wrapped_select_key(i, b): 
        return select_key(items_copy[i], bins_copy[b])

    for item_idxs_sublist, bin_idxs_sublist in _split_problem(item_idxs, 
                                                              bin_idxs, split):

        item_idxs_sublist.sort(key=lambda i: item_key(items_copy[i]))

        bin_idxs_sublist.sort(key=lambda b: bin_key(bins_copy[b]))

        pack(items_copy, item_idxs_sublist, bins_copy, bin_idxs_sublist, 
             wrapped_select_key, mapping)

    return mapping


def pack_by_items(items=[], bins=[], 
                  select_key=zero, item_key=zero, bin_key=zero, split=1):
    return _pack(items, bins,
                 _pack_by_items, select_key, item_key, bin_key, split,
                [None] * len(items))


def pack_by_bins(items=None, bins=None, 
                 select_key=zero, item_key=zero, bin_key=zero, split=1):
    return _pack(items, bins,
                 _pack_by_bins, select_key, item_key, bin_key, split,
                 [None] * len(items))


def pack_by_product(items=None, bins=None, 
                    select_key=zero, item_key=zero, bin_key=zero, split=1):
    return _pack(items, bins,
                 _pack_by_product, select_key, item_key, bin_key, split,
                 [None] * len(items))


PACKS_BY_NAME = {
    "pack_by_items"   : pack_by_items,
    "pack_by_bins"    : pack_by_bins,
    "pack_by_product" : pack_by_product,
}


def list_packs():
    return PACKS_BY_NAME.keys()


def get_pack_by_name(name):
    return PACKS_BY_NAME[name]
