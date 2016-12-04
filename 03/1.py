from itertools import permutations
import numpy as np
import argparse
import os

def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    return parser

def is_valid(triangle):
    for permutation in permutations(triangle):
        if np.sum(permutation[0:2]) <= permutation[2]:
            return False
    return True

def main(args):
    with open(args.filename) as fd:
        data = fd.read().splitlines()

    triangles = [
        tuple(map(int, entry.split()))
        for entry in data
    ]


    valid_count = 0
    for triangle in triangles:
        if is_valid(triangle):
            valid_count += 1

    print(valid_count)



if __name__ == '__main__':
    args = build_parser().parse_args()
    assert os.path.isfile(args.filename), 'Must provide a valid filename'
    main(args)
