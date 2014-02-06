#!/usr/bin/env python3

from pyvpsolver import solve_mvbp

def pack_vectors(**kwargs):

    solver = kwargs.get('solver', 'glpk')
    verbose = kwargs.get('verbose', False)
    factor = kwargs.get('factor', 1000)

    problem = kwargs.get('problem', None)

    items = problem.get('items', None)
    bins = problem.get('bins', None)


    # FIXME: smarter handling of items of the same type...
    # brandao can only handle int contents...
    vpsolver_items = [[[int(factor * r) for r in item]] for item in items]

    bin_set = set(tuple(bin_) for bin_ in bins)
    if len(bin_set) != 1:
        # FIXME: well, for now...
        raise Exception('vpsolver can only work with homogeneous bins')

    vpsolver_bins = [tuple(int(factor * c) for c in bins[0])]

    b = [1] * len(items)
    cost = [1]

    script = "vpsolver_" + solver + ".sh"

    # FIXME: single for balance?
    _, sol = solve_mvbp(vpsolver_bins, vpsolver_items, b, cost, 
                        verbose=verbose, script=script)

    mapping = [None] * len(items)
    for b, (_, bin_contents) in enumerate(sol[0]):
        for i, _ in bin_contents:
            mapping[i] = b

    # FIXME: method names?
    return {
        'mapping' : mapping,
    }

def main(argv=None):
    pass

if __name__ == "__main__":
    main() 
