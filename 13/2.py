from itertools import permutations, combinations
import argparse
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
            break
        dist, current = frontier.get()
        visited_dist[current] = dist
        steps_prev = steps[current]

        if current == target:
            return True

        neighbours = get_neighbours(current)
        for neighbour in neighbours:
            neighbour_dist = math.sqrt(
                (neighbour[0] - target[0]) ** 2 +
                (neighbour[1] - target[1]) ** 2
            )
            if (neighbour not in visited_dist.keys() or
                    visited_dist[neighbour] > neighbour_dist):
                if steps_prev < 50:
                    frontier.put((neighbour_dist, neighbour))
                    steps[neighbour] = steps_prev + 1
    return False

def main():
    coords = [
        (x, y)
        for x in range(0, 52)
        for y in range(0, 52)
        if not filled(x,y)
    ]
    reachables = 0
    for coord in coords:
        if search((1, 1), coord):
            reachables += 1
    print(reachables)

if __name__ == '__main__':
    main()
