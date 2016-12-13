from __future__ import print_function
import numpy as np
import argparse
import time
import re
import os

def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')

    parser.add_argument(
        '--part2',
        action='store_true'
    )
    return parser


def filled(x, y, num=10):
    poly = x*x + 3*x + 2*x*y + y + y*y
    bin_string = '{:b}'.format(poly+num)
    one = re.compile('1')
    ones = re.findall(one, bin_string)
    if ones is None:
        even = True
    else:
        even = ((len(ones) % 2) == 0)
    return not even


def main(args):
    with open(args.filename) as fd:
        data = fd.read().splitlines()

    grid = np.zeros((7, 10))

    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            if filled(x, y):
                print('#', end='')
            else:
                print('.', end='')
        print()

if __name__ == '__main__':
    args = build_parser().parse_args()
    assert os.path.isfile(args.filename), 'Must provide a valid filename'
    main(args)
