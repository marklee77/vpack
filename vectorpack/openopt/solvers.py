#!/usr/bin/env python3

from openopt import BPP

def pack_vectors(**kwargs):

    solver = kwargs.get('solver', 'glpk')
    iprint = kwargs.get('iprint', -1)

    problem = kwargs.get('problem', None)

    items = problem.get('items', None)
    bins = problem.get('bins', None)

    # FIXME: smarter handling of items of the same type...
    openopt_items = [dict([('name', i), ('n', 1)] + 
                          [('d{:d}'.format(d), r) for d, r in enumerate(item)])
                     for i, item in enumerate(items)]

    bin_set = set(tuple(bin_) for bin_ in bins)
    if len(bin_set) != 1:
        raise Exception('openopt can only work with homogeneous bins')

    openopt_bins = dict(
        [('d{:d}'.format(d), c) for d, c in enumerate(bins[0])] +
        [('n', len(bins))]
    )

    openopt_prob = BPP(openopt_items, openopt_bins)

    openopt_result = openopt_prob.solve(solver, iprint=iprint)

    mapping = [None] * len(items)
    for b, bin_contents in enumerate(openopt_result.xf):
        for i, count in bin_contents.items():
            mapping[i] = b

    # FIXME: method names?
    return {
        'mapping' : mapping,
    }
