from multiprocessing import Process, Manager
import sys
import re

class Bot:
    def __init__(self, init_string, registry, m, maxsize=2, target=[17, 61]):
        self.name, self.low_dest, self.high_dest = re.findall(
            r'((?:bot|output) \d+)',
            init_string
        )
        self.registry = registry
        self.registry[self.name] = self
        self.queue = m.Queue(maxsize=maxsize)
        self.target = target

    def transfer_chips(self):
        print('yo')
        items = [self.queue.get() for _ in range(self.queue.qsize())]

        if items == self.target:
            print(self.name)

        print(self.registry[self.low_dest])
        self.registry[self.low_dest].put(items[0])
        self.registry[self.high_dest].put(items[1])

    def work(self):
        print(self)
        while True:
            if self.queue.full():
                print('Blah')
                sys.stdout.flush()
                self.transfer_chips()


class OutBin:
    def __init__(self, m):
        self.queue = m.Queue()


if __name__ == '__main__':
    m = Manager()
    registry = m.dict()
    registry['output 0'] = OutBin(m) # OutBin(m)
    registry['output 1'] = OutBin(m)
    # registry['output 1'] = m.Queue() # OutBin(m)
    print(registry['output 1'])
    # bot = Bot('bot 2 gives low to output 0 and high to output 1', registry, m)


    # bot.queue.put(17)
    # bot.queue.put(61)
    # p = Process(target=bot.work)
    # p.start()
    # print('Here')
    # print(bot.queue)
    # sys.stdout.flush()
    # p.join()
