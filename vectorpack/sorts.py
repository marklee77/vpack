from functools import partial, reduce

import operator

try:
    from sys import maxint 
except ImportError:
    # python3 workaround
    from sys import maxsize as maxint

from yaml import load as yload

import numpy as np

from .util import negate_func, zero


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
    "prod"      : lambda v: reduce(operator.mul, v, 1),
    "lnorm"     : np.linalg.norm,
    "max"       : max,
    "maxratio"  : maxratio,
    "imaxratio" : imaxratio,
    "maxdiff"   : maxdiff
}


def list_sort_keys():
    return sorted(SORT_KEYS_BY_NAME.keys())


def get_sort_key_by_name(name):
    return SORT_KEYS_BY_NAME[name]


def parse_sort_cmdline(sortcmd):
    args = sortcmd.split(":")

    arg = args.pop(0)
    desc = False
    if arg in [ "a", "d" ]:
        if arg is "d":
            desc = True
        arg = args.pop(0)

    sort_key = get_sort_key_by_name(arg)

    kwargs = {}
    if args:
        kwargs.update(yload("\n".join(arg.replace('=', ': ') for arg in args)))

    if desc:
        return partial(negate_func, sort_key, **kwargs)

    if kwargs:
        return partial(sort_key, **kwargs)

    return sort_key
