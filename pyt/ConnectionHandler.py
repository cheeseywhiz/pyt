import multiprocessing
import xcffib
from xcffib import xproto
from .Logger import Logger

__all__ = 'ConnectionHandler',


class ConnectionHandler(xcffib.Connection):
    # provides basic main loop handler
    # user of class wraps xinit and handle_event
    def __init__(self, *args, event_queue=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.event_queue = event_queue
        self.event_process = multiprocessing.Process(
            target=self.queue_x_events, daemon=True)

    def queue_x_events(self):
        Logger.debug('queue_x_events')

        while True:
            event = self.wait_for_event()
            self.event_queue.put(event)

    def start_event_process(self):
        self.event_process.start()
        return self

    def __enter__(self):
        return self \
            .xinit() \
            .flush() \
            .start_event_process()

    def __exit__(self, exc_type, exc_value, traceback):
        super().disconnect()

    def flush(self):
        super().flush()
        return self

    def xinit(self):
        return self

    def handle_event(self, event):
        for func in [id, type, vars]:
            Logger.debug(func(event))

        if isinstance(event, xproto.DestroyNotifyEvent):
            return False

        return True

    def handle_next_event(self):
        event = self.event_queue.get()
        loop_is_not_done = self.handle_event(event)
        self.flush()
        return loop_is_not_done

    def run(self):
        with self:
            while self.handle_next_event():
                pass
