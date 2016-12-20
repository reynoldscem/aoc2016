# from multiprocessing import Process, Manager
from threading import Thread
from random import random
from queue import Queue
import argparse
import time
import os
import re

class Bot:
    def __init__(self, init_string, registry, maxsize=2, target=['17', '61']):
        self.name, self.low_dest, self.high_dest = re.findall(
            r'((?:bot|output) \d+)',
            init_string
        )

        registry[self.name] = self
        self.registry = registry
        self.queue = Queue(maxsize=maxsize)
        self.target = target
        self.blocked = False

    def transfer_chips(self, registry):
        self.blocked = True
        items = [self.queue.get() for _ in range(self.queue.qsize())]
        items = list(map(str, sorted(list(map(int, items)))))
        self.blocked = False
        print('{} transferring {}'.format(self.name, sorted(items)))

        if items == self.target:
            print('GOAL! {} transferring {}'.format(self.name, items))
            return True

        self.blocked = True
        registry[self.low_dest].queue.put(items[0])
        self.blocked = False
        self.blocked = True
        registry[self.high_dest].queue.put(items[1])
        self.blocked = False

    def work(self, registry):
        found = False
        while not found:
            time.sleep(random() * 0.05)
            if self.queue.full():
                if self.transfer_chips(registry):
                    found = True


class OutBin:
    def __init__(self):
        self.queue = Queue()
        self.registry = None


def build_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('filename')

    return parser


def main(args):
    assert os.path.isfile(args.filename), 'File must exist.'
    with open(args.filename) as fd:
        data = fd.read().splitlines()

    bot_def_lines = [
        line for line in data
        if line.startswith('bot')
    ]

    registry = dict()
    threads = []
    for bot_def_line in bot_def_lines:
        outputs = map(
            int,
            re.findall(
                r'(?:output (\d+))',
                bot_def_line
            )
        )

        for out_idx in outputs:
            string = 'output {}'.format(out_idx)
            if string not in registry.keys():
                registry[string] = OutBin()

        bot = Bot(bot_def_line, registry)
        thread = Thread(target=bot.work, args=(registry,), daemon=True)
        threads.append(thread)

    value_lines = [
        line for line in data
        if line.startswith('value')
    ]

    receiving_bots = []
    for line in value_lines:
        value, bot_id = re.findall(r'\d+', line)
        registry['bot {}'.format(bot_id)].queue.put(value)
        receiving_bots.append(bot_id)

    for thread in threads:
        thread.start()

    found = False

    while not found:
        for thread in threads:
            if not thread.is_alive():
                found = True

        blocked = 0
        bots = [name for name in registry.keys() if name.startswith('bot')]
        for name in bots:
            if name.startswith('bot'):
                blocked += 1 if registry[name].blocked else 0
        time.sleep(0.5)
        print('{} / {} blocked'.format(blocked, len(bots)))


if __name__ == '__main__':
    args = build_parser().parse_args()
    main(args)
