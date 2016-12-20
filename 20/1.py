import argparse
import os

def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')

    parser.add_argument(
        '--log',
        action='store_true'
    )

    return parser

def main(args):
    with open(args.filename) as fd:
        data = fd.read().splitlines()

    data = sorted(
        [
            list(map(int, line.split('-')))
            for line in data
        ]
    )
    idx = 0
    while True:
        if idx == len(data) - 1:
            break

        first, second = data[idx], data[idx + 1]

        if second[0] <= first[1] + 1:
            data[idx] = [first[0], max(first[1], second[1])]
            del data[idx + 1]
            if args.log:
                print('Combining, {} and {}'.format(first, second))
                print('Now {}'.format(data[idx]))
                print('Data now {} long'.format(len(data)))
        else:
            idx += 1

    print('Part 1:')
    print(data[0][1] + 1)
    print()

    accumulator = 0
    for idx in range(len(data) - 1):
        diff = (data[idx+1][0] - (data[idx][1] + 1))
        accumulator += diff
        if args.log:
            print(
                'Difference between {} and {} is {}'.format(
                    data[idx], data[idx+1], diff
                )
            )

    print('Part 2:')
    print(accumulator)

if __name__ == '__main__':
    args = build_parser().parse_args()
    assert os.path.isfile(args.filename), 'Must provide a valid filename'
    main(args)
