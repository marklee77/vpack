from math import ceil

def bound_lc(problem=None):

    if problem is None:
        return None

    items = problem['items']
    bins = problem['bins']

    return max(int(ceil(float(sum(itemdim)) / max(bindim))) 
               for itemdim, bindim in zip(zip(*items), zip(*bins)))

