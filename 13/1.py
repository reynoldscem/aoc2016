from __future__ import print_function
from itertools import permutations
import numpy as np
import argparse
import time
import re
import os

from queue import Queue

def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')

    parser.add_argument(
        '--part2',
        action='store_true'
    )
    return parser


def filled(x, y, num=10):
    poly = x*x + 3*x + 2*x*y + y + y*y
    bin_string = '{:b}'.format(poly+num)
    one = re.compile('1')
    ones = re.findall(one, bin_string)
    if ones is None:
        even = True
    else:
        even = ((len(ones) % 2) == 0)
    return not even


def valid(move, grid):
    if filled(*move):
        return False

    if move[0] < 0 or move[1] < 0:
        return False

    if move[0] > grid.shape[1]-1 or move[1] > grid.shape[0]-1:
        return False

    return True

def print_grid(grid):
    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            if grid[y, x] == 2:
                print('*', end='')
                continue
            if grid[y, x] == 3:
                print('^', end='')
                continue
            if filled(x, y):
                print('#', end='')
            else:
                print('.', end='')
        print()

perms = list(permutations([1, 0], 2)) + list(permutations([-1, 0], 2))
print(perms)
def get_neighbours(grid, current_pos):
    moves = [
        (current_pos[0] + perm[0], current_pos[1] + perm[1])
        for perm in perms
    ]
    moves = [
        move
        for move in moves
        if valid(move, grid)
    ]
    return moves

def search(start, grid, target):
    visited = set()
    frontier = Queue()

    frontier.put((start,0))

    while True:
        if frontier.empty():
            print(':(')
            break
        current, dist = frontier.get()
        visited.add(current)

        grid[current[1], current[0]] = 3
        print()
        print_grid(grid)
        print()
        input()

        if current == target:
            print(dist)
            return

        neighbours = get_neighbours(grid, current)
        print(neighbours)
        for neighbour in neighbours:
            if neighbour not in visited:
                frontier.put((neighbour, dist+1))

def main(args):
    with open(args.filename) as fd:
        data = fd.read().splitlines()

    grid = np.zeros((7, 10))

    grid[1, 1] = 2

    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            if grid[y, x] == 2:
                print('*', end='')
                continue
            if filled(x, y):
                print('#', end='')
                grid[y, x] = 1
            else:
                print('.', end='')
                grid[y, x] = 0
        print()
    current_pos = np.array([1, 1])
    neighbours = get_neighbours(grid, current_pos)

    for neighbour in neighbours:
        grid[neighbour[1], neighbour[0]] = 3

    print()
    print_grid(grid)
    search((1,1), grid, (7,4))

    import ipdb; ipdb.set_trace()

if __name__ == '__main__':
    args = build_parser().parse_args()
    assert os.path.isfile(args.filename), 'Must provide a valid filename'
    main(args)
