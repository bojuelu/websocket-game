# coding: utf-8

import time


class Timer(object):
    def __init__(self):
        self.current = 0.0
        self.last = 0.0
        self.reset()
        pass

    def reset(self):
        t = time.time()
        self.current = t
        self.last = t
        pass

    def get_time(self):
        self.current = time.time()
        return self.current - self.last

    def is_above(self, sec, auto_reset):
        self.current = time.time()
        diff = self.current - self.last

        if diff >= sec:
            if auto_reset:
                self.reset()
            return True
        else:
            return False
    pass
