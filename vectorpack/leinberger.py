import packs

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

# FIXME: memcache?
def rank_to_dimension(v):
    """ compute the ordering on dimensions based on their size.
        e.g., for a 3D array [2, 0, 1] means that the dimension 2 has the
        largest value, dimension 0 the next, and dimension 1 the smallest.

        The natural ordering is used to break any ties and thus guarantee a
        stable sort. 
    """
    return sorted(range(len(v)), key=lambda d: (-v[d], d)) # stable sort
    
# FIXME: memcache?
def dimension_to_rank(v):
    """ Provide map that is inverse of above, e.g., can be used to go from a
        dimension number to a rank for that dimension
    """
    d2r = [None] * len(v)
    for r, d in enumerate(rank_to_dimension(v)):
        d2r[d] = r
    return d2r

# FIXME: memcache?
def pp_select(item=None, capacity=None, window_size=None):
    if window_size is None:
        window_size = len(capacity)
    elif window_size == 0:
        return None
    r2d_c = rank_to_dimension(capacity)
    d2r_i = dimension_to_rank(item)
    return [d2r_i[d] for d in r2d_c[:window_size]]

# FIXME: memcache?
def cp_select(item=None, capacity=None, window_size=None):
    if window_size is None:
        window_size = len(capacity)
    elif window_size == 0:
        return None
    largest_capacity_dims = set(rank_to_dimension(capacity)[:window_size])
    largest_item_dims = set(rank_to_dimension(item)[:window_size])
    return -len(largest_capacity_dims & largest_item_dims)

def permutation_pack(
    items=None, boxes=None, item_key=None, box_key=None, window_size=None):
    if item_key is None:
        item_key = lambda x: 0
    select_key = lambda item, capacity: (
        pp_select(item=item, capacity=capacity, window_size=window_size),
        item_key(item))
    return packs.pack_best_fit_by_boxes(
        items=items, boxes=boxes, box_key=box_key, select_key=select_key)

def choose_pack(
    items=None, boxes=None, item_key=None, box_key=None, window_size=None):
    if item_key is None:
        item_key = lambda x: 0
    select_key = lambda item, capacity: (
        cp_select(item=item, capacity=capacity, window_size=window_size),
        item_key(item))
    return packs.pack_best_fit_by_boxes(
        items=items, boxes=boxes, box_key=box_key, select_key=select_key)

