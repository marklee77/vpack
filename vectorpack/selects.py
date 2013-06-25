from leinberger import pp_select, cp_select

SELECTS_BY_NAME = {
    "asum"       : (lambda i, c: sum(c - i)),
    "al2"        : (lambda i, c: norm(c - i, ord=2)),
    "amax"       : max,
    "amaxratio"  : (lambda i, c: float(max(c - i)) / min(c - i)),
    "amaxdiff"   : (lambda v: max(v) - min(v)),
    "none"       : None,
    "dsum"       : (lambda v: -sum(v)),
    "dl2"        : (lambda v: -norm(v, ord=2)),
    "dmax"       : (lambda v: -max(v)),
    "dmaxtratio" : (lambda v: float(min(v)) / max(v)),
    "dmaxdiff"   : (lambda v: min(v) - max(v)),
    "pp"         : ,
    "cp"         :
}
