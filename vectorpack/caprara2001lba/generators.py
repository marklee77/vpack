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
    num_dimensions = kwargs.get('num_dimensions', 2)
    num_items = kwargs.get('num_items', 0)
    num_bins = kwargs.get('num_bins', 0)
    cls = kwargs.get('cls', 1)

    if num_bins == 0:
        num_bins = num_items

    random.seed(seed) 

    items = []
    bins = []

    if cls < 7:
        if cls == 1:
            alpha = 100
            beta = 400
        elif cls == 2:
            alpha = 1
            beta = 1000
        elif cls == 3:
            alpha = 200
            beta = 800
        elif cls == 4:
            alpha = 50
            beta = 200
        elif cls == 5:
            alpha = 25
            beta = 100
        elif cls == 6:
            alpha = 20
            beta = 100
        if cls < 6:
            capacity = 1000
        else:
            capacity = 150

        items = [[random.randint(alpha, beta) 
                  for i in range(num_dimensions)] 
                 for j in range(num_items)]

        bins = [[capacity] * num_dimensions] * num_bins

    elif cls < 9:
        if num_dimensions != 2:
            raise SystemExit("Generalizing instances from class " +
                             str(num_dimensions) + 
                             " to other than 2 dimensions is not supported.")
        if cls == 7:
            for i in range(num_items):
                w = random.randint(20, 100)
                v = random.randint(w - 10, w + 10)
                items.append([w, v])
        else:
            for i in range(num_items):
                w = random.randint(20, 100)
                v = random.randint(110 - w, 130 - w)
                items.append([w, v])
        bins = [[150, 150]] * num_bins

    elif cls == 9:
        items = [[random.randint(100, 400) 
                  for i in range(num_dimensions)] 
                 for j in range(num_items)]
        dimtotals = [sum(dim) for dim in zip(*items)]
        L = int(ceil(float(max(dimtotals))/1000))
        caps = [int(ceil(float(dimtotal)/L)) for dimtotal in dimtotals]
        bins = [caps] * num_bins
        pass

    elif cls == 10:
        if num_items % 3 != 0:
            raise SystemExit("Class 10 requires number of items to be a " +
                             "multiple of 3")
        
        items = [[random.randint(25, 50) 
                  for i in range(num_dimensions)] 
                 for j in range(num_items // 3 * 2)]

        for i in range(num_items // 3):
            items.append([100 - items[2*i][d] - items[2*i+1][d]
                         for d in range(num_dimensions)])

        bins = [[100] * num_dimensions] * num_bins

    return {
        'note' : 'Caprara and Toth, Class ' + str(cls),
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
    parser.add_argument('-i', '--num_items', type=int, required=True, 
                        help='number of items')
    parser.add_argument('-c', '--class', type=int, default=1, dest='cls',
                        help='class number from Caprara and Toth 2001')
    parser.add_argument('-d', '--num_dimensions', type=int, default=2,
                        help='number of dimensions')

    args = parser.parse_args()

    print(dump(generate_problem(**args.__dict__), Dumper=Dumper), end='')

if __name__ == "__main__":
    main()

