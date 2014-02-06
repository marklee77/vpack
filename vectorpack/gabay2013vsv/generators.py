from argparse import ArgumentParser
from hashlib import sha1
from math import ceil

import random

from yaml import dump
try:
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Dumper

from vsvbp.generator import generator, unif_bin

def generate_problem(**kwargs):

    genargs = kwargs.copy()
    family = genargs.pop('family', None)

    seed = genargs.pop('seed', -1)
    num_bins = genargs.pop('num_bins', 0)
    num_resources = genargs.pop('num_resources', 1)
    min_fill = genargs.pop('min_fill', 0.8)
    bin_generator = genargs.pop('bin_generator', unif_bin)

    instance = generator(num_bins, num_resources, min_fill, 
                         bin_generator=bin_generator, seed=seed, **genargs)

    items = [tuple(item.requirements[:]) for item in instance.items]
    bins = [tuple(bin_.capacities[:]) for bin_ in instance.bins]

    return {
        'argshash' : 
            sha1(str(sorted(list(kwargs.items()))).encode('utf-8')).hexdigest(),
        'args' : kwargs,
        'bins' : bins,
        'items' : items,
    }

def main(argv=None):

    parser = ArgumentParser(description="Generate a random problem instance.")
    parser.add_argument('-s', '--seed', type=int, default=1337,
                        help='seed for random number generator')
    parser.add_argument('-d', '--num_dimensions', type=int, default=1,
                        help='number of dimensions')
    parser.add_argument('-b', '--num_bins', type=int, required=True, 
                        help='number of bins')
    parser.add_argument('-i', '--num_items', type=int, required=True, 
                        help='number of items')
    parser.add_argument('-c', '--cov', type=float, default=0.0, 
                        help='bin dimension cov')
    parser.add_argument('-k', '--slack', type=float, default=0.4, help='slack')
    parser.add_argument('-n', '--note', help='note')

    args = parser.parse_args()

    print(dump(generate_problem(**args.__dict__), Dumper=Dumper), end='')

if __name__ == "__main__":
    main()

