from argparse import ArgumentParser
from hashlib import sha1
from math import ceil

import random

from yaml import dump
try:
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Dumper

def generate_problem(**kwargs):

    seed = kwargs.get('seed', 1)
    num_dimensions = kwargs.get('num_dimensions', 1)
    num_bins = kwargs.get('num_bins', 0)
    num_items = kwargs.get('num_items', 0)
    cov = kwargs.get('cov', 0.0)
    slack = kwargs.get('slack', 0.4)
    
    random.seed(seed) 

    bins = [[max(1, min(int(random.normalvariate(50, 50 * cov)), 100))
              for i in range(num_dimensions)]
              for j in range(num_bins)]

    bindim_totals = [sum(bin_[i] for bin_ in bins) 
                     for i in range(num_dimensions)]

    items = [[random.randint(1, 100) for i in range(num_dimensions)] 
             for j in range(num_items)]

    itemdim_totals = [sum(item[i] for item in items)
                      for i in range(num_dimensions)]

    for item in items:
        for i in range(num_dimensions):
            item[i] = max(1, int(item[i] * (1.0 - slack) * 
                                    bindim_totals[i] / itemdim_totals[i]))

    return {
        'argshash' : 
            sha1(str(sorted(list(kwargs.items()))).encode('utf-8')).hexdigest(),
        'args' : kwargs,
        'bins' : bins,
        'items' : items
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

