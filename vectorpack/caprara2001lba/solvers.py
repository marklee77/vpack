#!/usr/bin/env python3

from argparse import ArgumentParser

from yaml import load as yload, dump as ydump

try:
    from yaml import CLoader as Loader
except ImportError:
    from yaml import Loader

try:
    from yaml import CDumper as Dumper
except ImportError:
    from yaml import Dumper

def pack_vectors(**kwargs):
    pass


def main(argv=None):

    parser = ArgumentParser(description="Solve a vector packing problem.")

if __name__ == "__main__":
    main() 
