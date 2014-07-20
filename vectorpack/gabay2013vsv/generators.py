from argparse import ArgumentParser
from hashlib import sha1
from math import ceil

import random

from yaml import dump
try:
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Dumper

import vsvbp.generator as generator

def generate_problem(**kwargs):

    genkwargs = kwargs.copy()

    _ = genkwargs.pop('family', None)

    seed = genkwargs.pop('seed', -1)
    num_bins = genkwargs.pop('num_bins', 0)
    num_resources = genkwargs.pop('num_resources', 1)
    min_fill = genkwargs.pop('min_fill', 0.8)
    bin_generator_name = genkwargs.pop('bin_generator', 'unif_bin')
    bin_generator = getattr(generator, bin_generator_name)

    instance = generator.generator(num_bins, num_resources, min_fill, 
                         bin_generator=bin_generator, seed=seed, **genkwargs)

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

    print(dump(generate_problem(**args.__dict__), Dumper=Dumper))

if __name__ == "__main__":
    main()

