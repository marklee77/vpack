from functools import wraps

from numpy.linalg import norm as lnorm

from .sorts import maxratio, maxdiff
from .util import zero

"""
    The basic approach from Leinberger 1999 is to find the most empty bin
    dimensions, those with the largest capacities available, and pack the bin
    with items that are largest in those dimensions
"""

def rank_to_dimension(v):
    """ compute the ordering on dimensions based on their size.
        e.g., for a 3D array [2, 0, 1] means that the dimension 2 has the
        largest value, dimension 0 the next, and dimension 1 the smallest.

        The natural ordering is used to break any ties and thus guarantee a
        stable sort. 
    """
    return sorted(range(len(v)), key=v.__getitem__, reverse=True)
    

def dimension_to_rank(v):
    """ Provide map that is inverse of above, e.g., can be used to go from a
        dimension number to a rank for that dimension
    """
    d2r = [None] * len(v)
    for r, d in enumerate(rank_to_dimension(v)):
        d2r[d] = r
    return d2r


def pp_select(item, bin_, window_size=None):
    if window_size is None:
        window_size = len(bin_)
    elif window_size == 0:
        return None
    d2r_i = dimension_to_rank(item)
    r2d_b = rank_to_dimension(bin_)
    return [d2r_i[d] for d in r2d_b[:window_size]]


def cp_select(item, bin_, window_size=None):
    if window_size is None:
        window_size = len(bin_)
    elif window_size == 0:
        return None
    largest_item_dims = set(rank_to_dimension(item)[:window_size])
    largest_bin_dims = set(rank_to_dimension(bin_)[:window_size])
    return -len(largest_item_dims & largest_bin_dims)

def make_select(f, *args, **kwargs):

    @wraps(f)
    def f_select(item, bin_):
        return f(bin_ - item, *args, **kwargs)

    return f_select

SELECTS_BY_NAME = {
    "none"       : zero,
    "sum"        : make_select(sum),
    "lnorm"      : make_select(lnorm),
    "max"        : make_select(max),
    "maxratio"   : make_select(maxratio),
    "maxdiff"    : make_select(maxdiff),
    "pp"         : pp_select,
    "cp"         : cp_select,
}


def list_selects():
    return SELECTS_BY_NAME.keys()


def get_select_by_name(name):
    return SELECTS_BY_NAME[name]

