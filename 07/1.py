from collections import deque
import numpy as np
import argparse
import os
import re


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    return parser


def window(seq, n=4):
     it = iter(seq)
     win = deque((next(it, None) for _ in range(n)), maxlen=n)
     yield win
     append = win.append
     for e in it:
         append(e)
         yield win


def has_abba(string):
    if string[0] == string[1]:
        return False
    if string[0] != string[-1]:
        return False
    if string[1] != string[-2]:
        return False

    print('String {} has abba'.format(string))
    return True


def windowed_abba(string):
    for sub_chars in window(string):
        sub_str = ''.join(sub_chars)
        if has_abba(sub_str):
            return True
    return False


def has_hypernet_abba(string):
    hypernet = re.compile('\[(\w*)\]')

    hypernet_matches = re.findall(hypernet, string)

    for hypernet_match in hypernet_matches:
        if windowed_abba(hypernet_match):
            return True

    return False


def supports_tls(string):
    if has_hypernet_abba(string):
        return False

    hypernet = re.compile('\[(\w*)\]')

    strings = re.sub(hypernet, ';', string).split(';')

    for string in strings:
        if windowed_abba(string):
            return True
    return False


def main(args):
    with open(args.filename) as fd:
        data = fd.read().splitlines()

    count = sum(map(supports_tls, data))

    print(count)


if __name__ == '__main__':
    args = build_parser().parse_args()
    assert os.path.isfile(args.filename), 'Must provide a valid filename'
    main(args)
