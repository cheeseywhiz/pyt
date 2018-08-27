import logging
import multiprocessing
import os
import sys
from .make_process import make_process

__all__ = 'Logger'


class QueueLogHandler(logging.Handler):
    def __init__(self, message_queue):
        super().__init__(logging.NOTSET)
        fmt = logging.Formatter('%(name)s: %(process)d: %(levelname)s: '
                                '%(message)s')
        super().setFormatter(fmt)
        self.message_queue = message_queue

    def emit(self, record):
        message = super().format(record)
        self.message_queue.put(message)


@make_process(daemon=True)
def print_messages(message_queue):
    print(f'Starting logger on PID {os.getpid()}')

    while True:
        message = message_queue.get()
        print(message, file=sys.stderr)


def instantiate(cls):
    message_queue = multiprocessing.Queue()
    print_messages(message_queue)
    return cls(message_queue)


@instantiate
class Logger(logging.Logger):
    def __init__(self, message_queue):
        super().__init__('pyt')
        handler = QueueLogHandler(message_queue)
        super().addHandler(handler)
