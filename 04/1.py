from collections import Counter
import argparse
import os
import re

def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    return parser


def get_checksum(entry):
    split_entry = entry.split('-')
    name_chars = ''.join(sorted(''.join(split_entry[:-1])))
    checksum = ''.join(sorted(Counter(name_chars))[:5])
    return ''.join([
        v[0]
        for v in sorted(Counter(name_chars).items(),
        key=lambda kv: (-kv[1], kv[0]))
    ][:5])

def main(args):
    with open(args.filename) as fd:
        data = fd.read().splitlines()

    accum = 0
    for line in data:
        checksum = get_checksum(line)
        given_checksum = re.findall(r'\[(.+)\]', line)[0]

        if checksum == given_checksum:
            num = int(re.findall(r'(\d+)', line)[0])
            accum += num

    print(accum)


if __name__ == '__main__':
    args = build_parser().parse_args()
    assert os.path.isfile(args.filename), 'Must provide a valid filename'
    main(args)
