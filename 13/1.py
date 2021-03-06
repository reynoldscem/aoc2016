from __future__ import print_function
from itertools import permutations
import math
import re
import os

from queue import Queue


def filled(x, y, num=1364):
    poly = x*x + 3*x + 2*x*y + y + y*y
    bin_string = '{:b}'.format(poly+num)
    one = re.compile('1')
    ones = re.findall(one, bin_string)
    if ones is None:
        even = True
    else:
        even = ((len(ones) % 2) == 0)
    return not even


def valid(move):
    if filled(*move):
        return False

    if move[0] < 0 or move[1] < 0:
        return False

    return True

perms = list(permutations([1, 0], 2)) + list(permutations([-1, 0], 2))
def get_neighbours(current_pos):
    moves = [
        (current_pos[0] + perm[0], current_pos[1] + perm[1])
        for perm in perms
    ]
    moves = [
        move
        for move in moves
        if valid(move)
    ]
    return moves

def search(start, target):
    visited_dist = {}
    steps = {}
    frontier = Queue()

    frontier.put((0, start))
    steps[start] = 0

    iterations = 0
    while True:
        iterations += 1
        if frontier.empty():
            print(':(')
            break
        dist, current = frontier.get()
        visited_dist[current] = dist
        steps_prev = steps[current]

        if current == target:
            print('This heuristic took {} its'.format(iterations))
            print(steps_prev)
            return

        neighbours = get_neighbours(current)
        for neighbour in neighbours:
            neighbour_dist = math.sqrt(
                (neighbour[0] - target[0]) ** 2 +
                (neighbour[1] - target[1]) ** 2
            )
            if (neighbour not in visited_dist.keys() or
                    visited_dist[neighbour] > neighbour_dist):
                frontier.put((neighbour_dist, neighbour))
                steps[neighbour] = steps_prev + 1

def main():
    search((1,1), (31, 39))

if __name__ == '__main__':
    main()
