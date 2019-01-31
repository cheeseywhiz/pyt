from ... import actions
from ...Logger import Logger
from ...make_process import make_process
from .TerminalStore import TerminalStore

__all__ = 'run_terminal'


@make_process
def run_terminal(terminal_queue, redraw_event, action_queue, write_queue):
    Logger.debug('run_terminal')
    store = TerminalStore(terminal_queue, redraw_event)

    while True:
        action = action_queue.get()
        Logger.debug(action)

        if isinstance(action, actions.Quit):
            break
        elif isinstance(action, actions.KeyboardInput):
            write_queue.put(action.keyboard_input.encode())
            continue

        store.dispatch(action)

    Logger.debug('run_terminal done')
