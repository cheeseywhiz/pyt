import queue
import random
import redux
import sys
import time
import threading
from .Terminal import Terminal
from . import actions
from .Logger import Logger
from .Connection import Connection

__all__ = 'main',


def slow_dispatch(dispatch):
    def run():
            for line in sys.stdin:
                time.sleep(random.random())
                dispatch(actions.PutByteSequence(map(ord, line)))

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
    event_queue = queue.Queue()
    store = TerminalStore(event_queue)
    connection = Connection(event_queue=event_queue)
    thread = threading.Thread(target=slow_dispatch(store.dispatch))
    thread.start()
    connection.run()
    thread.join()


if __name__ == '__main__':
    main()
