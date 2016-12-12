import numpy as np
import argparse
import time
import os

def build_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')

    parser.add_argument(
        '--part2',
        action='store_true'
    )
    return parser

def main(args):
    with open(args.filename) as fd:
        data = fd.read().splitlines()

    instructions = [instruction.split() for instruction in data]

    registers = dict(zip('abcd', [0]*4))

    if args.part2:
        registers['c'] = 1

    pc = 0

    while pc < len(data):
        instr = instructions[pc]
        if instr[0] == 'cpy':
            if instr[1] in registers.keys():
                registers[instr[-1]] = registers[instr[1]]
            else:
                registers[instr[-1]] = int(instr[1])
            pc += 1
            continue
        if instr[0] == 'inc':
            registers[instr[1]] += 1
            pc += 1
            continue
        if instr[0] == 'dec':
            registers[instr[1]] -= 1
            pc += 1
            continue
        if instr[0] == 'jnz':
            if instr[1] in registers.keys():
                if registers[instr[1]] != 0:
                    pc += int(instr[-1])
                    continue
            else:
                if int(instr[1]) != 0:
                    pc += int(instr[-1])
                    continue
            pc += 1
            continue

    print(registers)

if __name__ == '__main__':
    args = build_parser().parse_args()
    assert os.path.isfile(args.filename), 'Must provide a valid filename'
    main(args)
