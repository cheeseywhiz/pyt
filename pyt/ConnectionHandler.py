import multiprocessing
import xcffib
from xcffib import xproto

__all__ = 'ConnectionHandler',


class ConnectionHandler(xcffib.Connection):
    # provides basic main loop handler
    # user of class wraps xinit and handle_event
    def __init__(self, *args, event_queue=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.event_queue = event_queue

    def queue_x_events(self):
        while True:
            event = self.wait_for_event()
            self.event_queue.put(event)

    def __enter__(self):
        multiprocessing.Process(target=self.queue_x_events,
                                daemon=True).start()
        return self.xinit().flush()

    def __exit__(self, exc_type, exc_value, traceback):
        super().disconnect()

    def flush(self):
        super().flush()
        return self

    def xinit(self):
        return self

    def handle_event(self, event):
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
