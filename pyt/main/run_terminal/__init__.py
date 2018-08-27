import random
import time
from ... import actions
from ...Logger import Logger
from ...make_process import make_process
from .TerminalStore import TerminalStore

__all__ = 'run_terminal'


@make_process
def run_terminal(terminal_queue, redraw_event):
    Logger.debug('run_terminal')
    store = TerminalStore(terminal_queue, redraw_event)

    with open('typescript', 'rb') as file:
        for line in file:
            time.sleep(random.random())
            store.dispatch(actions.PutByteSequence(line))

    Logger.debug('run_terminal done')
