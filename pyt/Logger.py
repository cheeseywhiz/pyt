import logging
import multiprocessing
import os
import sys

__all__ = 'Logger',


class QueueLogHandler(logging.Handler):
    def __init__(self, message_queue):
        super().__init__(logging.INFO)
        fmt = logging.Formatter('%(name)s: %(process)d: %(levelname)s: '
                                '%(message)s')
        super().setFormatter(fmt)
        self.message_queue = message_queue

    def emit(self, record):
        message = super().format(record)
        self.message_queue.put(message)


def print_messages(message_queue):
    def run():
        print(f'Starting logger on PID {os.getpid()}')

        while True:
            message = message_queue.get()
            print(message, file=sys.stderr)

    return run


def instantiate(cls):
    message_queue = multiprocessing.Queue()
    multiprocessing.Process(target=print_messages(message_queue),
                            daemon=True).start()
    return cls(message_queue)


@instantiate
class Logger(logging.Logger):
    def __init__(self, message_queue):
        super().__init__('pyt')
        handler = QueueLogHandler(message_queue)
        super().addHandler(handler)
