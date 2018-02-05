import threading
from time import sleep

import random

threadLimiter = threading.BoundedSemaphore(10)


class ThreadLib(threading.Thread):
    def __init__(self, threat, name, **kwargs):
        threading.Thread.__init__(self)
        self.threadID = threat
        self.name = name
        self.kwargs = kwargs

    def run(self):
        threadLimiter.acquire()

        try:
            if 'callback' in self.kwargs:
                self.kwargs.get('callback')(self.kwargs.get('param'))
        finally:
            threadLimiter.release()


def callback(data):
    sleep(random.randint(0, 5))
    print(data)

if __name__ == '__main__':
    a = ThreadLib(1, 'hello', callback=callback, param="asaswa")
    a.start()
    a = ThreadLib(1, 'hello', callback=callback, param="asas12")
    a.start()
    print('hai')
