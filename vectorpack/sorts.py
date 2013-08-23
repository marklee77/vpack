try:
    from sys import maxint 
except ImportError:
    # python3 workaround
    from sys import maxsize as maxint

from numpy.linalg import norm as lnorm

from .util import zero

def maxratio(v):
    maxval = max(v)
    minval = min(v)
    if minval == 0.0:
        return float('inf')
    return float(maxval) / minval

def imaxratio(v):
    maxval = max(v)
    minval = min(v)
    if minval == 0.0:
        return maxint
    return 1000 * maxval // minval

def maxdiff(v):
    return max(v) - min(v)

SORT_KEYS_BY_NAME = {
    "none"      : zero,
    "sum"       : sum,
    "lnorm"     : lnorm,
    "max"       : max,
    "maxratio"  : maxratio,
    "imaxratio" : imaxratio,
    "maxdiff"   : maxdiff
}

def list_sort_keys():
    return sorted(SORT_KEYS_BY_NAME.keys())

def get_sort_key_by_name(name):
    return SORT_KEYS_BY_NAME[name]
