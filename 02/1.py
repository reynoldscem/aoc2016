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

    actions = {
        'U': (lambda pos: (np.max((0, pos[0] - 1)), pos[1])),
        'D': (lambda pos: (np.min((2, pos[0] + 1)), pos[1])),
        'L': (lambda pos: (pos[0], np.max((0, pos[1] - 1)))),
        'R': (lambda pos: (pos[0], np.min((2, pos[1] + 1))))
    }

    pos = [1, 1];
    buttons = np.arange(1, 10).reshape((3, 3))

    code = []
    for line in data:
        for char in line:
            pos = actions[char](pos)
        code.append(buttons[pos])
    print(''.join(map(str, code)))


if __name__ == '__main__':
    args = build_parser().parse_args()
    assert os.path.isfile(args.filename), 'Must provide a valid filename'
    main(args)
