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
    return ''.join([
        v
        for v, _ in sorted(Counter(name_chars).items(),
        key=lambda kv: (-kv[1], kv[0]))
    ][:5])

def main(args):
    with open(args.filename) as fd:
        data = fd.read().splitlines()

    for line in data:
        checksum = get_checksum(line)
        given_checksum = re.findall(r'\[(.+)\]', line)[0]

        if checksum == given_checksum:
            rot = int(re.findall(r'(\d+)', line)[0])
            encrypted_words = line.split('-')
            decrypted = ' '.join([
                ''.join(map(
                    lambda x: chr((((ord(x) - 97) + rot) % 26) + 97),
                    word
                ))
                for word in encrypted_words
            ])
            # Just print decrypted names and sector IDs
            # pipe into "grep north"
            print('{}: {}'.format(decrypted, rot))


if __name__ == '__main__':
    args = build_parser().parse_args()
    assert os.path.isfile(args.filename), 'Must provide a valid filename'
    main(args)
