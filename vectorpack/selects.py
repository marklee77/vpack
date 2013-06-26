from leinberger import pp_select, cp_select

SELECTS_BY_NAME = {
    "asum"       : (lambda i, c: sum(c - i)),
    "al2"        : (lambda i, c: norm(c - i, ord=2)),
    "amax"       : (lambda i, c: max(c - i)),
    "amaxratio"  : (lambda i, c: float(max(c - i)) / min(c - i)),
    "amaxdiff"   : (lambda i, c: max(c - i) - min(c - i)),
    "none"       : None,
    "dsum"       : (lambda i, c: -sum(c - i)),
    "dl2"        : (lambda i, c: -norm(c - i, ord=2)),
    "dmax"       : (lambda i, c: -max(c - i)),
    "dmaxtratio" : (lambda i, c: float(min(c - i)) / max(c - i)),
    "dmaxdiff"   : (lambda i, c: min(c - i) - max(c - i)),
    "pp"         : pp_select,
    "cp"         : cp_select
}

def get_select_names():
    return SELECTS_BY_NAME.keys()

def get_select(name):
    return SELECTS_BY_NAME.get(name, None)
