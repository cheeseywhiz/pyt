import redux
from .Logger import Logger
from .Terminal import Terminal

__all__ = 'TerminalStore',


class TerminalStore(redux.Store):
    def __init__(self, terminal_queue, redraw_event):
        super().__init__(Terminal())
        self.terminal_queue = terminal_queue
        self.redraw_event = redraw_event
        self.sub_queue_state()
        self.sub_log_state()

    def queue_state(self):
        self.terminal_queue.put(self.state)
        self.redraw_event.set()

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
