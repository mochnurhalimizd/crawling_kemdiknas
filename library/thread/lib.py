import threading
from time import sleep

import random


class ThreadLib(threading.Thread):
    def __init__(self, threat, name, **kwargs):
        threading.Thread.__init__(self)
        self.threadID = threat
        self.name = name
        self.kwargs = kwargs

    def run(self):
        if 'callback' in self.kwargs:
            self.kwargs.get('callback')(self.kwargs.get('param'))


def callback(data):
    sleep(random.randint(0, 5))
    print(data)

if __name__ == '__main__':
    a = ThreadLib(1, 'hello', callback=callback, param="asaswa")
    a.start()
    a = ThreadLib(1, 'hello', callback=callback, param="asas12")
    a.start()
    print('hai')
