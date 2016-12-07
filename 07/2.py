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
     yield ''.join(win)
     append = win.append
     for e in it:
         append(e)
         yield ''.join(win)


def is_aba(string):
    if len(string) != 3:
        return False
    if string[0] != string[-1]:
        return False
    if string[0] == string[1]:
        return False
    return True


def get_bab(string):
    return string[1] + string[0] + string[1]

def get_required_babs(in_data):
    abas = []

    if type(in_data) is list:
        for item in in_data:
            abas += get_required_babs(item)
    elif type(in_data) is str:
        for sub_str in window(in_data, 3):
            if is_aba(sub_str):
                abas.append(get_bab(sub_str))

    return abas

def supports_ssl(string):
    hypernet = re.compile('\[(\w*)\]')

    strings = re.sub(hypernet, ';', string).split(';')

    babs = get_required_babs(strings)

    hypernet_strings = re.findall(hypernet, string)

    for hypernet_string in hypernet_strings:
        for bab in babs:
            if bab in window(hypernet_string, 3):
                return True

    return False


def main(args):
    with open(args.filename) as fd:
        data = fd.read().splitlines()

    count = sum(map(supports_ssl, data))

    print(count)


if __name__ == '__main__':
    args = build_parser().parse_args()
    assert os.path.isfile(args.filename), 'Must provide a valid filename'
    main(args)
