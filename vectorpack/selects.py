from functools import partial
from hashlib import sha1
from numpy.linalg import norm

def pairkey_null(v1, v2):
    return 0

# FIXME: get_select implement pre-caching and calculation...

"""
Some notes:

    suppose bin as 

    r2d_c 1 3 0 2 then d2r_c 2 0 3 1

    item preference

    May need to discuss...

    r2d_i    d2r_c[r2d_i]  d2r_i    d2r_i[r2d_c]
    -------  ------------  -------  ------------
    1 3 0 2  0 1 2 3       2 0 3 1  0 1 2 3
    1 3 2 0  0 1 3 2       3 0 2 1  0 1 3 2
    1 0 3 2  0 2 1 3       1 0 3 2  0 2 1 3
    1 2 3 0  0 3 1 2       3 0 1 2  0 2 3 1
    1 0 2 3  0 2 3 1       1 0 2 3  0 3 1 2
    1 2 0 3  0 3 2 1       2 0 1 3  0 3 2 1
    3 1 0 2  1 0 2 3       2 1 3 0  1 0 2 3
    3 1 2 0  1 0 3 2       3 1 2 0  1 0 3 2
    0 1 3 2  2 0 1 3       0 1 3 2  1 2 0 3
    2 1 3 0  3 0 1 2       3 1 0 2  1 2 3 0
    0 1 2 3  2 0 3 1       0 1 2 3  1 3 0 2
    2 1 0 3  3 0 2 1       2 1 0 3  1 3 2 0
    3 0 1 2  1 2 0 3       1 2 3 0  2 0 1 3
    3 2 1 0  1 3 0 2       3 2 1 0  2 0 3 1
    0 3 1 2  2 1 0 3       0 2 3 1  2 1 0 3
    2 3 1 0  3 1 0 2       3 2 0 1  2 1 3 0
    0 2 1 3  2 3 0 1       0 2 1 3  2 3 0 1
    2 0 1 3  3 2 0 1       1 2 0 3  2 3 1 0
    3 0 2 1  1 2 3 0       1 3 2 0  3 0 1 2
    3 2 0 1  1 3 2 0       2 3 1 0  3 0 2 1
    0 3 2 1  2 1 3 0       0 3 2 1  3 1 0 2
    2 3 0 1  3 1 2 0       2 3 0 1  3 1 2 0
    0 2 3 1  2 3 1 0       0 3 1 2  3 2 0 1
    2 0 3 1  3 2 1 0       1 3 0 2  3 2 1 0
    
    d2r_i[r2d_c] seems better, as it preserves largest positioning first,
    then within each block of 6 preserves 2nd largest next...

"""



"""
    The basic approach from Leinberger 1999 is to find the most empty bin
    dimensions, those with the largest capacities available, and pack the bin
    with items that are largest in those dimensions
"""

""" FIXME: this *could* speed things up for item lookups d2r, but it doesn't
    seem like it... """
def memoize(function):
    cache = {}
    def decorated_function(v):
        argshash = sha1(v).digest()
        if argshash in cache:
            return cache[argshash]
        else:
            val = function(v)
            cache[argshash] = val
            return val
    return decorated_function

@memoize
def dimension_to_rank2(v):
    """ Provide map that is inverse of above, e.g., can be used to go from a
        dimension number to a rank for that dimension
    """
    d2r = [None] * len(v)
    for r, d in enumerate(sorted(range(len(v)), key=lambda d: (-v[d], d))):
        d2r[d] = r
    return d2r

def rank_to_dimension(v):
    """ compute the ordering on dimensions based on their size.
        e.g., for a 3D array [2, 0, 1] means that the dimension 2 has the
        largest value, dimension 0 the next, and dimension 1 the smallest.

        The natural ordering is used to break any ties and thus guarantee a
        stable sort. 
    """
    return sorted(range(len(v)), key=lambda d: (-v[d], d)) # stable sort
    
def dimension_to_rank(v):
    """ Provide map that is inverse of above, e.g., can be used to go from a
        dimension number to a rank for that dimension
    """
    d2r = [None] * len(v)
    for r, d in enumerate(rank_to_dimension(v)):
        d2r[d] = r
    return d2r

def pp_select(item=None, capacity=None, window_size=None):
    if window_size is None:
        window_size = len(capacity)
    elif window_size == 0:
        return None
    r2d_c = rank_to_dimension(capacity)
    d2r_i = dimension_to_rank(item)
    return [d2r_i[d] for d in r2d_c[:window_size]]


def cp_select(item=None, capacity=None, window_size=None):
    if window_size is None:
        window_size = len(capacity)
    elif window_size == 0:
        return None
    largest_capacity_dims = set(rank_to_dimension(capacity)[:window_size])
    largest_item_dims = set(rank_to_dimension(item)[:window_size])
    return -len(largest_capacity_dims & largest_item_dims)


SELECTS_BY_NAME = {
    "asum"       : (lambda i, c: sum(c - i)),
    "al2"        : (lambda i, c: norm(c - i, ord=2)),
    "amax"       : (lambda i, c: max(c - i)),
    "amaxratio"  : (lambda i, c: float(max(c - i)) / min(c - i)),
    "amaxdiff"   : (lambda i, c: max(c - i) - min(c - i)),
    "none"       : pairkey_null,
    "dsum"       : (lambda i, c: -sum(c - i)),
    "dl2"        : (lambda i, c: -norm(c - i, ord=2)),
    "dmax"       : (lambda i, c: -max(c - i)),
    "dmaxratio"  : (lambda i, c: float(min(c - i)) / max(c - i)),
    "dmaxdiff"   : (lambda i, c: min(c - i) - max(c - i)),
    "pp"         : pp_select,
    "pp:w1"      : partial(pp_select, window_size=1),
    "cp"         : cp_select,
    "cp:w1"      : partial(cp_select, window_size=1),
}


def get_select_names():
    return SELECTS_BY_NAME.keys()


# FIXME: use "partial" for keyword parameter passing
def get_select(name):
    return SELECTS_BY_NAME.get(name, None)
