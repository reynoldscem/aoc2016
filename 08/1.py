from __future__ import print_function
import numpy as np
import argparse
import os
import re


def build_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('filename')

    return parser


# Mask col. Get col vector. Roll by amount.
# Reapply.
def rot_col(rect, x, v):
    vec = np.copy(rect[:, x])
    new_rect = np.copy(rect)
    new_rect[:, x] = 0.
    vec = np.roll(vec, v)
    new_rect[:, x] = vec
    return new_rect


# Copy array. Roll in rows.
# Mask back original row.
# Add in new rect.
def rot_row(rect, y, v):
    row_mask = np.ones(rect.shape[0], dtype=np.bool)
    row_mask[y] = 0

    shift = np.copy(rect)
    preserve = np.copy(rect)

    preserve[~row_mask, :] = 0
    shift[row_mask, :] = 0

    shifted = np.roll(shift, v)

    return np.logical_or(shifted, preserve)


def make_rect(r=6, c=50):
    return np.zeros((r, c))


def mask_ab(rect, a, b):
    mask = np.ones((b, a))

    new_rect = np.copy(rect)
    new_rect[0:b, 0:a] = mask

    return new_rect


def print_rect(rect):
    for row in rect:
        for entry in row:
            if entry == 1:
                print('#', end='')
            else:
                print('.', end='')
        print()


def execute_line(rect, line):
    print(line)
    function_lookup = {
        'rect': mask_ab,
        'rotate column': rot_col,
        'rotate row': rot_row
    }

    expression = re.compile(
        r'(rect|rotate row|rotate column) x?y?=?(\d+) ?\w+ ?(\d+)'
    )
    res = re.findall(expression, line)[0]
    print(res)

    return function_lookup[res[0]](rect, int(res[1]), int(res[2]))


def main(args):
    with open(args.filename) as fd:
        data = fd.read().splitlines()

    rect = make_rect()
    print_rect(rect)

    for line in data:
        input()
        rect = execute_line(rect, line)
        print_rect(rect)

    print(np.sum(rect))


if __name__ == '__main__':
    args = build_parser().parse_args()
    assert os.path.isfile(args.filename), 'Must provide a valid filename'
    main(args)
