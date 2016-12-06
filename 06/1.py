from collections import Counter
import numpy as np
import argparse
import os


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    return parser


def main(args):
    with open(args.filename) as fd:
        data = fd.read().splitlines()

    char_arr = np.asarray(list(map(list, data))).transpose()

    result = ''.join([
        Counter(string).most_common(1)[0][0]
        for string in char_arr
    ])

    print(result)


if __name__ == '__main__':
    args = build_parser().parse_args()
    assert os.path.isfile(args.filename), 'Must provide a valid filename'
    main(args)
