from multiprocessing import Process, Manager
import argparse
import os
import re

class Bot:
    def __init__(self, init_string, registry, m, maxsize=2, target=[2, 5]):
        self.name, self.low_dest, self.high_dest = re.findall(
            r'((?:bot|output) \d+)',
            init_string
        )

        registry[self.name] = self
        self.registry = registry
        self.queue = m.Queue(maxsize=maxsize)
        self.target = target

    def transfer_chips(self, registry):
        items = [self.queue.get() for _ in range(self.queue.qsize())]

        if items == self.target:
            print(self.name)
            return True

        print(registry)
        registry[self.low_dest].queue.put(items[0])
        registry[self.high_dest].queue.put(items[1])

    def work(self, registry):
        print('Work')
        print(registry)
        found = False
        while not found:
            if self.queue.full():
                found = self.transfer_chips(registry)


class OutBin:
    def __init__(self, m):
        self.queue = m.Queue()
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

    m = Manager()
    registry = dict()
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
                registry[string] = OutBin(m)

        bot = Bot(bot_def_line, registry, m)
        p = Process(target=bot.work, args=(registry,))
        p.start()

    for bot in registry.values():
        print(bot.registry)
    print(registry)
    value_lines = [
        line for line in data
        if line.startswith('value')
    ]

    for line in value_lines:
        value, bot_id = re.findall(r'\d+', line)
        registry['bot {}'.format(bot_id)].queue.put(value)

    p.join()


if __name__ == '__main__':
    args = build_parser().parse_args()
    main(args)
