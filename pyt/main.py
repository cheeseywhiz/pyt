import multiprocessing
from .Logger import Logger
from .Connection import Connection
from .run_terminal import run_terminal

__all__ = 'main',


def main():
    Logger.debug('GUI')
    terminal_queue = multiprocessing.Queue()
    redraw_event = multiprocessing.Event()
    connection = Connection(terminal_queue=terminal_queue,
                            redraw_event=redraw_event)
    proc = run_terminal(terminal_queue, redraw_event)
    connection.run()
    proc.join()
