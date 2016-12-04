import numpy as np
import argparse
import os

def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    return parser

VALID = np.array([
    [0, 0, 1, 0, 0],
    [0, 1, 1, 1, 0],
    [1, 1, 1, 1, 1],
    [0, 1, 1, 1, 0],
    [0, 0, 1, 0, 0]
])

ACTIONS = {
    'U': (lambda pos: (np.max((0, pos[0] - 1)), pos[1])),
    'D': (lambda pos: (np.min((4, pos[0] + 1)), pos[1])),
    'L': (lambda pos: (pos[0], np.max((0, pos[1] - 1)))),
    'R': (lambda pos: (pos[0], np.min((4, pos[1] + 1))))
}

BUTTONS = np.array(list(
    '  1  '
    ' 234 '
    '56789'
    ' ABC '
    '  D  '
)).reshape((5, 5))

def main(args):
    with open(args.filename) as fd:
        data = fd.read().splitlines()

    pos = [2, 0];

    code = []
    for line in data:
        for char in line:
            new_pos = ACTIONS[char](pos)
            pos = new_pos if VALID[new_pos] else pos
        code.append(BUTTONS[pos])
    print(''.join(code))


if __name__ == '__main__':
    args = build_parser().parse_args()
    assert os.path.isfile(args.filename), 'Must provide a valid filename'
    main(args)
