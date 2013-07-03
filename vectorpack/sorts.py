from numpy.linalg import norm as lnorm

from .util import zero, negate_func

def maxratio(v):
    maxval = max(v)
    minval = min(v)
    if minval == 0.0:
        return float('inf')
    return float(maxval) / minval

def maxdiff(v):
    return max(v) - min(v)

SORT_KEYS_BY_NAME = {
    "none"      : zero,
    "sum"       : sum,
    "lnorm"     : lnorm,
    "max"       : max,
    "maxratio"  : maxratio,
    "maxdiff"   : maxdiff
}

def list_sort_keys():
    return sorted(SORT_KEYS_BY_NAME.keys())

# FIXME: move to packs?
def wrap_sort_key_func(f):
    def sort_key_func(vlist, idx):
        return f(vlist[idx])
    return sort_key_func

# FIXME: move to script?
# FIXME: vlist...
def get_sort_key(name, vlist=None):
    from functools import partial
    from yaml import load as yload
    args = name.split(":")
    desc = False
    arg = args.pop(0)
    if arg in [ "a", "d" ]:
        if arg is "d":
            desc = True
        arg = args.pop(0)
    # FIXME: exception handler
    f = wrap_sort_key_func(SORT_KEYS_BY_NAME[arg])
    kwargs = { 'vlist': vlist }
    if args:
        kwargs.update(yload("\n".join(arg.replace('=', ': ') for arg in args)))
    if desc:
        return partial(negate_func, f, **kwargs)
    return partial(f, **kwargs)
