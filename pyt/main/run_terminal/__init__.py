import random
import time
from ... import actions
from ...Logger import Logger
from ...make_process import make_process
from .TerminalStore import TerminalStore

__all__ = 'run_terminal'


@make_process
def run_terminal(terminal_queue, redraw_event, action_queue):
    Logger.debug('run_terminal')
    store = TerminalStore(terminal_queue, redraw_event)

    with open('typescript', 'rb') as file:
        for line in file:
            action_queue.put(actions.PutByteSequence(line))

    while True:
        action = action_queue.get()

        if isinstance(action, actions.Quit):
            break
        elif isinstance(action, actions.KeyboardInput):
            # TODO: write to pty
            pass

        time.sleep(random.random())
        store.dispatch(action)

    Logger.debug('run_terminal done')
