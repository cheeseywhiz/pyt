import queue
import threading
import xcffib
from xcffib import xproto

__all__ = 'ConnectionHandler',


class EventQ(queue.Queue):
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.thread = threading.Thread(target=self.put_x_events, daemon=True)

    def start(self):
        self.thread.start()

    def put_x_events(self):
        while True:
            event = self.connection.wait_for_event()
            self.put(event)


class ConnectionHandler(xcffib.Connection):
    # provides basic main loop handler
    # user of class wraps xinit and handle_event
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.event_q = EventQ(self)

    def __enter__(self):
        self.event_q.start()
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
        event = self.event_q.get()
        loop_is_not_done = self.handle_event(event)
        self.flush()
        self.event_q.task_done()
        return loop_is_not_done

    def run(self):
        with self:
            while self.handle_next_event():
                pass
