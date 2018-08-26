from .Logger import Logger
from .ConnectionBase import ConnectionBase
from .make_process import make_process

__all__ = 'redraw_window',


class RedrawWindowConnection(ConnectionBase):
    def __init__(self, *args, redraw_event=None, window_id=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.redraw_event = redraw_event
        self.window_id = window_id

    def loop(self):
        while True:
            self.redraw_event.wait()
            super().redraw().flush()
            self.redraw_event.clear()


@make_process(daemon=True)
def redraw_window(redraw_event, window_id):
    Logger.debug('redraw_window')

    RedrawWindowConnection(
        redraw_event=redraw_event, window_id=window_id,
    ).run()
