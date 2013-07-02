from numpy.linalg import norm

def key_null(v):
    return 0

SORTS_BY_NAME = {
    "asum"       : sum,
    "al2"        : (lambda v: norm(v, ord=2)),
    "amax"       : max,
    "amaxratio"  : (lambda v: float(max(v)) / min(v)),
    "amaxdiff"   : (lambda v: max(v) - min(v)),
    "none"       : key_null,
    "dsum"       : (lambda v: -sum(v)),
    "dl2"        : (lambda v: -norm(v, ord=2)),
    "dmax"       : (lambda v: -max(v)),
    "dmaxratio"  : (lambda v: float(min(v)) / max(v)),
    "dmaxdiff"   : (lambda v: min(v) - max(v))
}

def get_sort_names():
    return SORTS_BY_NAME.keys()

def get_sort(name):
    return SORTS_BY_NAME.get(name, None)
