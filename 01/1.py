import numpy as np
import argparse
import os

def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    return parser

def main(args):
    with open(args.filename) as fd:
        data = fd.read().split(', ')

    instructions = map(
        lambda x: (x[0], int(x[1:])),
        data
    )

    north = np.array([0, 1])
    rot_r = np.array([[0, 1], [-1, 0]])
    rot_l = -rot_r

    actions = {
        'R': rot_r,
        'L': rot_l
    }

    pos = [0, 0]
    ori = [0, 1]

    for turn, move in instructions:
        ori = actions[turn].dot(ori)
        pos += move * ori

    print(np.sum(np.abs(pos)))

if __name__ == '__main__':
    args = build_parser().parse_args()
    assert os.path.isfile(args.filename), 'Must provide a valid filename'
    main(args)
