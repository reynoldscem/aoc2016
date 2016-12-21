import argparse
import os
import re

def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    return parser


def swap_pos(password, ind1, ind2):
    password = list(password)
    password[ind1], password[ind2] = password[ind2], password[ind1]
    return ''.join(password)


def swap_letter(password, letter1, letter2):
    ind1 = password.find(letter1)
    ind2 = password.find(letter2)
    password = list(password)
    password[ind1], password[ind2] = password[ind2], password[ind1]
    return ''.join(password)

def reverse_positions(password, ind1, ind2):
    return ''.join((
        password[:ind1],
        password[ind1:ind2+1][::-1],
        password[ind2+1:]
    ))


def rotate_str(password, direction, amount):
    amount = amount % len(password)
    if direction == 'right':
        return password[-amount:] + password[:-amount]

    return password[amount:] + password[:amount]


def move_pos(password, from_pos, to_pos):
    password = list(password)
    password.insert(to_pos, password.pop(from_pos))
    return ''.join(password)


def rotate_on_letter(password, rotate_letter):
    position = password.find(rotate_letter)
    if position >= 4:
        return rotate_str(password, 'right', position+2)
    else:
        return rotate_str(password, 'right', position+1)


def process(line, password):
    swap_pos_match = re.match(
        'swap position (\d+) with position (\d+)',
        line
    )
    if swap_pos_match is not None:
        return swap_pos(
            password,
            int(swap_pos_match.group(1)),
            int(swap_pos_match.group(2))
        )

    swap_letter_match = re.match(
        'swap letter ([a-z]) with letter ([a-z])',
        line
    )
    if swap_letter_match is not None:
        return swap_letter(
            password,
            swap_letter_match.group(1),
            swap_letter_match.group(2)
        )

    reverse_str_match = re.match(
        'reverse positions (\d+) through (\d+)',
        line
    )
    if reverse_str_match is not None:
        return reverse_positions(
            password,
            int(reverse_str_match.group(1)),
            int(reverse_str_match.group(2))
        )

    rotate_str_match = re.match(
        'rotate (left|right) (\d+) steps?',
        line
    )
    if rotate_str_match is not None:
        return rotate_str(
            password,
            rotate_str_match.group(1),
            int(rotate_str_match.group(2))
        )

    move_pos_match = re.match(
        'move position (\d+) to position (\d+)',
        line
    )
    if move_pos_match is not None:
        return move_pos(
            password,
            int(move_pos_match.group(1)),
            int(move_pos_match.group(2))
        )

    rotate_on_letter_match = re.match(
        'rotate based on position of letter ([a-z])',
        line
    )
    if rotate_on_letter_match is not None:
        return rotate_on_letter(
            password,
            rotate_on_letter_match.group(1)
        )


def main(args):
    with open(args.filename) as fd:
        data = fd.read().splitlines()

    password = 'abcdefgh'
    # print(password)

    for line in data:
        password = process(line, password)
        # print(password)

    print(password)


if __name__ == '__main__':
    args = build_parser().parse_args()
    assert os.path.isfile(args.filename), 'Must provide a valid filename'
    main(args)
