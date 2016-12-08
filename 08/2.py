from __future__ import print_function
import numpy as np
import argparse
import time
import os
import re


def build_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('filename')

    return parser


def rot_col(rect, x, v):
    vec = np.copy(rect[:, x])
    new_rect = np.copy(rect)
    new_rect[:, x] = 0
    vec = np.roll(vec, v)
    new_rect[:, x] = vec
    return new_rect


def rot_row(rect, y, v):
    vec = np.copy(rect[y, :])
    new_rect = np.copy(rect)
    new_rect[y, :] = 0
    vec = np.roll(vec, v)
    new_rect[y, :] = vec
    return new_rect


def make_rect(r=6, c=50):
    return np.zeros((r, c), dtype=np.bool)


def mask_ab(rect, a, b):
    mask = np.ones((b, a))
    new_rect = np.copy(rect)
    new_rect[0:b, 0:a] = mask
    return new_rect


def print_rect(rect):
    for row in rect:
        for entry in row:
            if entry:
                print(u'\u2588', end='')
            else:
                print(' ', end='')
        print()


def execute_line(rect, line):
    function_lookup = {
        'rect': mask_ab,
        'rotate column': rot_col,
        'rotate row': rot_row
    }

    expression = re.compile(
        r'(rect|rotate row|rotate column) x?y?=?(\d+) ?\w+ ?(\d+)'
    )
    res = re.findall(expression, line)[0]

    return function_lookup[res[0]](rect, int(res[1]), int(res[2]))


def main(args):
    with open(args.filename) as fd:
        data = fd.read().splitlines()

    rect = make_rect()
    print_rect(rect)

    for line in data:
        rect = execute_line(rect, line)
        print_rect(rect)
        time.sleep(0.06)

    print(np.sum(rect))


if __name__ == '__main__':
    args = build_parser().parse_args()
    assert os.path.isfile(args.filename), 'Must provide a valid filename'
    main(args)
