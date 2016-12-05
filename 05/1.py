from itertools import count
import argparse
import hashlib
import os


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    return parser


def keygen(data):
    for i in count():
        m = hashlib.md5()
        m.update(
            '{}{}'.format(data, i).encode('utf-8')
        )
        hash_val = m.hexdigest()
        if hash_val.startswith('0' * 5):
            yield hash_val[5]


def main(args):
    with open(args.filename) as fd:
        data = fd.read().rstrip()

    gen = keygen(data)

    password = ''.join(next(gen) for _ in range(8))

    print(password)


if __name__ == '__main__':
    args = build_parser().parse_args()
    assert os.path.isfile(args.filename), 'Must provide a valid filename'
    main(args)
