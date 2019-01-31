import io
import multiprocessing
import os
from .. import actions
from ..Logger import Logger
from ..make_process import make_process
from .Connection import Connection
from .run_terminal import run_terminal

__all__ = 'main'


@make_process(daemon=True)
def write_master(master, write_queue):
    Logger.debug('write_master')

    while True:
        buf = write_queue.get()
        os.write(master, buf)


@make_process(daemon=True)
def read_master(master, action_queue):
    Logger.debug('read_master')
    buf_size = io.DEFAULT_BUFFER_SIZE

    while True:
        buf = os.read(master, buf_size)
        action_queue.put(actions.PutByteSequence(buf))


def execsh():
    sh = os.getenv('SHELL', '/bin/sh')
    os.execvp(sh, [sh])


def new_pty():
    pid, master = os.forkpty()

    if not pid:  # child
        execsh()
    else:  # parent
        Logger.debug('shell pid = %d', pid)
        return master


def main():
    master = new_pty()
    Logger.start()
    Logger.debug('GUI')
    action_queue = multiprocessing.Queue()
    read_master(master, action_queue)
    terminal_queue = multiprocessing.Queue()
    write_queue = multiprocessing.Queue()
    write_master(master, write_queue)
    redraw_event = multiprocessing.Event()
    connection = Connection(terminal_queue=terminal_queue,
                            redraw_event=redraw_event,
                            action_queue=action_queue)
    proc = run_terminal(terminal_queue, redraw_event, action_queue,
                        write_queue)
    connection.run()
    proc.join()
