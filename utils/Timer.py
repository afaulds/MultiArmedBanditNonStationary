import time


class Timer:
    t = {}

    @staticmethod
    def start(key=""):
        Timer.t[key] = time.time()

    @staticmethod
    def pause(key=""):
        pass

    @staticmethod
    def stop(key="", print_output=True):
        duration = time.time() - Timer.t[key]
        if print_output:
            print("{}: {:.2f}s".format(key, duration))
