import multiprocessing
import random
import redux
import time
from .Terminal import Terminal
from . import actions
from .Logger import Logger
from .Connection import Connection

__all__ = 'main',


def run_terminal(terminal_queue):
    def run():
        Logger.debug('run_terminal')
        store = TerminalStore(terminal_queue)

        with open('typescript', 'rb') as file:
            for line in file:
                time.sleep(random.random())
                store.dispatch(actions.PutByteSequence(line))

        Logger.debug('run_terminal done')

    return run


class TerminalStore(redux.Store):
    def __init__(self, terminal_queue):
        super().__init__(Terminal())
        self.terminal_queue = terminal_queue
        self.sub_queue_state()
        self.sub_log_state()

    def queue_state(self):
        self.terminal_queue.put(self.state)

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
    Logger.debug('GUI')
    terminal_queue = multiprocessing.Queue()
    connection = Connection(terminal_queue=terminal_queue)
    proc = multiprocessing.Process(target=run_terminal(terminal_queue))
    proc.start()
    connection.run()
    proc.join()


if __name__ == '__main__':
    main()
