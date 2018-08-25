import random
import redux
import time
import threading
from .Terminal import Terminal
from . import actions
from .Connection import Connection

__all__ = 'main',


class SlowSendTerminal(threading.Thread):
    def run(self):
        connection, terminal = self._args
        time.sleep(random.uniform(1, 3))
        connection.event_q.put(terminal)


class TerminalStore(redux.Store):
    def __init__(self):
        super().__init__(Terminal())
        self.subscribe_print_state()

    def print_state(self):
        print(self.state)
        print(self.state.screen_str)

    def subscribe_print_state(self):
        self._unsubscribe_print_state = super().subscribe(self.print_state)

    def unsubscribe_print_state(self):
        self._unsubscribe_print_state()


def main():
    store = TerminalStore()

    with open('typescript', 'rb') as file:
        store.dispatch(actions.PutByteSequence(file.read()))

    connection = Connection()
    thread = SlowSendTerminal(args=(connection, store.state))
    thread.start()
    connection.run()
    thread.join()


if __name__ == '__main__':
    main()
