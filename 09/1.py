from __future__ import print_function
import numpy as np
import argparse
import time
import os
import re

import ipdb


def build_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('filename')

    return parser


def main(args):
    with open(args.filename) as fd:
        data = fd.read().rstrip()

    pattern = re.compile(r'\(\d+x\d+\)')
    digits = re.compile(r'\d+')
    paren = re.compile(r'^[^\(]+')

    res = ''
    while True:
        m = paren.match(data)
        if m is not None:
            res += data[m.start():m.end()]
            data = data[m.end():]
        m = pattern.search(data)
        if m is None:
            break
        specifier = data[m.start():m.end()]
        subseq_len, repeat_num = map(int, re.findall(digits, specifier))

        data = data[m.end():]

        subseq = data[0:subseq_len]
        data = data[subseq_len:]
        res += subseq * repeat_num


    print(res)
    print(len(res))


if __name__ == '__main__':
    args = build_parser().parse_args()
    assert os.path.isfile(args.filename), 'Must provide a valid filename'
    main(args)
