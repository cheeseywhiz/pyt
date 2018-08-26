import multiprocessing
import random
import redux
import time
from .Terminal import Terminal
from . import actions
from .Logger import Logger
from .Connection import Connection

__all__ = 'main',


def slow_dispatch(dispatch):
    def run():
        with open('typescript', 'rb') as file:
            for line in file:
                time.sleep(random.random())
                dispatch(actions.PutByteSequence(line))

    return run


class TerminalStore(redux.Store):
    def __init__(self, event_queue):
        super().__init__(Terminal())
        self.event_queue = event_queue
        self.sub_queue_state()
        self.sub_log_state()

    def queue_state(self):
        self.event_queue.put(self.state)

    def log_state(self):
        Logger.debug(self.state)
        Logger.debug(self.state.screen_str)

    def sub_queue_state(self):
        self._unsub_queue_state = super().subscribe(self.queue_state)

    def unsub_queue_state(self):
        self._unsub_queue_state()

    def sub_log_state(self):
        self._unsub_log_state = super().subscribe(self.log_state)

    def unsub_log_state(self):
        self._unsub_log_state()


def main():
    event_queue = multiprocessing.Queue()
    store = TerminalStore(event_queue)
    connection = Connection(event_queue=event_queue)
    proc = multiprocessing.Process(target=slow_dispatch(store.dispatch))
    proc.start()
    connection.run()
    proc.join()


if __name__ == '__main__':
    main()
