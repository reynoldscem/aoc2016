from itertools import count
from functools import lru_cache
import argparse
import hashlib
import os


@lru_cache(maxsize=None)
def get_hash(salt):
    m = hashlib.md5()
    m.update(salt.encode('utf-8'))
    return m.hexdigest()


@lru_cache(maxsize=None)
def has_triple(md5hash):
    for i in range(len(md5hash) - 2):
        sub_hash = md5hash[i:i+3]
        if sub_hash[0] == sub_hash[1] == sub_hash[2]:
            return sub_hash[0]

    return None


@lru_cache(maxsize=None)
def has_5_of_char(md5hash, char):
    for i in range(len(md5hash) - 4):
        sub_hash = md5hash[i:i+5]
        if sub_hash[0] == sub_hash[1] == sub_hash[2] == sub_hash[3] == sub_hash[4] == char:
            return True

    return False


def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    return parser


def main(args):
    with open(args.filename) as fd:
        data = fd.read().splitlines()
    salt = data[0]

    keys = []
    for idx in count():
        seed = salt + str(idx)
        md5hash = get_hash(seed)
        triple = has_triple(md5hash)
        if triple is not None:
            for search_idx in range(idx + 1, idx + 1001):
                search_seed = salt + str(search_idx)
                next_md5hash = get_hash(search_seed)
                if has_5_of_char(next_md5hash, triple):
                    print('Key at {}'.format(idx))
                    keys.append(idx)
                    break

        if len(keys) == 64:
            print(keys[-1])
            break


if __name__ == '__main__':
    args = build_parser().parse_args()
    assert os.path.isfile(args.filename), 'Must provide a valid filename'
    main(args)
