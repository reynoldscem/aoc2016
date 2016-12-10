from __future__ import print_function
from functools import lru_cache
import numpy as np
import argparse
import time
import sys
import os
import re

import ipdb


def build_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('filename')

    return parser


@lru_cache(maxsize=None)
def get_string_len(data):
    pattern = re.compile(r'\(\d+x\d+\)')
    digits = re.compile(r'\d+')
    paren = re.compile(r'^[^\(]+')

    m = pattern.search(data)
    if m is None:
        return len(data)
    pre_match = data[:m.start()]
    post_match = data[m.end():]
    specifier = data[m.start():m.end()]
    subseq_len, repeat_num = map(int, re.findall(digits, specifier))

    subseq = post_match[0:subseq_len]
    post_seq = post_match[subseq_len:]
    res = subseq * repeat_num

    return len(pre_match) + get_string_len(res) + get_string_len(post_seq)

def main(args):
    with open(args.filename) as fd:
        data = fd.read().rstrip()
    string_len = get_string_len(data)
    print(string_len)


if __name__ == '__main__':
    args = build_parser().parse_args()
    assert os.path.isfile(args.filename), 'Must provide a valid filename'
    main(args)
