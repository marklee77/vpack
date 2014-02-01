"""
.. module:: bounds
    :platform: Unix, Windows
    :synopsis: Functions to compute various VBPP bounds
.. moduleauthor:: Mark Stillwell <marklee@fortawesome.org>

"""

from math import ceil

import numpy as np

def bound_lc(problem=None):
    """This function computes the L_c bound as defined by Caprara and Toth 2001.

    Kwargs: 
        problem (dict): a vector packing problem instance

    Returns:
        int. The L_c bound on the number of bins required


    In fact, this function only computes L_c as defined by Caprary and Toth from
    problem instances with homogeneous bins, since this is the only case covered
    by them. Otherwise it's a little more optimistic than that even, estimating
    for the bin that has the maximum size in each dimension.
    """

    if problem is None:
        return None

    items = problem['items']
    bins = problem['bins']

    return max(int(ceil(float(sum(itemdim)) / max(bindim))) 
               for itemdim, bindim in zip(zip(*items), zip(*bins)))

def bound_l1(problem=None):
    """This function computes the L_1 bound as defined by Caprara and Toth 2001,
       using the procedure from Hammer and Mahadev 1985.

    Kwargs: 
        problem (dict): a vector packing problem instance

    Returns:
        int. The L_c bound on the number of bins required


    For the moment this is not implemented.
    """
    return None

def sweight(items=None):
    lambda_ = float(sum(item[0] for item in items)) / sum(sum(item) for item in items)
    return lambda_ * item[0] + (1 - lambda_) * item[1]

def bound_l2(problem=None):
    """This function computes the L_2 bound as defined by Caprara and Toth 2001.

    Kwargs: 
        problem (dict): a vector packing problem instance

    Returns:
        int. The L_2 bound on the number of bins required


    For the moment this is not implemented.
    """
    
    if problem is None:
        return None

    items = problem['items']
    bins = problem['bins']
    minsize = np.array([max(bindim) for bindim in zip(*bins)]) / 3

    S = []
    N_back_S = []
    for item in items:
        if (np.array(item) > minsize).all():
            S.append(item)
        else:
            N_back_S.append(item)

    # need to do sums for every pair in every dimension 
    for item in sorted(N_back_S, key=sweight, reverse=True):
        pass

    return None


