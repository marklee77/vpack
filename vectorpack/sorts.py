from functools import partial
from numpy.linalg import norm
from yaml import load as yload

def none_sort_key(i, vlist=None):
    return 0

def sum_sort_key(i, vlist=None):
    return sum(vlist[i])

def lnorm_sort_key(i, vlist=None, ord=2):
    return norm(vlist[i], ord=ord)

def max_sort_key(i, vlist=None):
    return max(vlist[i])

def maxratio_sort_key(i, vlist=None):
    return float(max(vlist[i]) / min(vlist[i]))

def maxdiff_sort_key(i, vlist=None):
    return max(vlist[i]) - min(vlist[i])

SORT_KEYS_BY_NAME = {
    "none"      : none_sort_key,
    "sum"       : sum_sort_key,
    "lnorm"     : lnorm_sort_key,
    "max"       : max_sort_key,
    "maxratio"  : maxratio_sort_key,
    "maxdiff"   : maxdiff_sort_key
}

def list_sort_keys():
    return sorted(SORT_KEYS_BY_NAME.keys())

def negate_func(f, *args, **kwargs):
    return -f(*args, **kwargs)

def get_sort_key(name, vlist=None):
    args = name.split(":")
    desc = False
    arg = args.pop(0)
    if arg in [ "a", "d" ]:
        if arg is "d":
            desc = True
        arg = args.pop(0)
    sort_key_func = SORT_KEYS_BY_NAME[arg] # FIXME: exception handler
    kwargs = { 'vlist': vlist }
    if args:
        kwargs.update(yload("\n".join(arg.replace('=', ': ') for arg in args)))
    if desc:
        return partial(negate_func, sort_key_func, **kwargs)
    return partial(sort_key_func, **kwargs)
