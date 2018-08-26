import xcffib
from xcffib import xproto
from .Logger import Logger

__all__ = 'ConnectionHandler',


class ConnectionHandler(xcffib.Connection):
    # provides basic main loop handler
    # user of class wraps xinit and handle_event
    def __enter__(self):
        return self \
            .xinit() \
            .flush()

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
        event = super().wait_for_event()
        loop_is_not_done = self.handle_event(event)
        self.flush()
        return loop_is_not_done

    def loop(self):
        while self.handle_next_event():
            pass

    def run(self):
        with self:
            self.loop()
