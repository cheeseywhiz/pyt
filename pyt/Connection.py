import queue
import sys
from xcffib import xproto
from .ConnectionBase import ConnectionBase
from . import config
from .redraw_window import redraw_window
from .ConnectionBase import window_check

__all__ = 'Connection',


class Connection(ConnectionBase):
    def __init__(self, *args, terminal_queue=None, redraw_event=None,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.terminal_queue = terminal_queue
        self.redraw_event = redraw_event
        self.terminal = None

    @window_check
    def redraw_window(self):
        redraw_window(self.redraw_event, self.window_id)
        return self

    def __enter__(self):
        return super().__enter__().redraw_window()

    def xinit(self):
        return super().xinit().init_font(
            name='fixed',
        ).new_window(
            n_cols=config.width,
            n_rows=config.height,
            attrs={
                xproto.CW.BackPixel: self.screen.black_pixel,
                xproto.CW.EventMask: (
                    xproto.EventMask.Exposure
                    | xproto.EventMask.StructureNotify)}
        ).init_wm(
            class_='pyt',
        ).create_gc({
            xproto.GC.Foreground: self.screen.white_pixel,
            xproto.GC.GraphicsExposures: False,
        }).map_window()

    def empty_terminal_queue(self, limit=None):
        """Empty the queue by getting as fast as we can. In case the queue
        becomes flooded, set a limit on how many times to get."""
        if limit is None:
            limit = sys.maxsize

        new_terminal = self.terminal_queue.get(block=False)

        for _ in range(limit):
            try:
                new_terminal = self.terminal_queue.get(block=False)
            except queue.Empty:
                return new_terminal

    def draw_terminal(self):
        try:
            new_terminal = self.empty_terminal_queue(24)
        except queue.Empty:
            pass
        else:
            self.terminal = new_terminal

        if self.terminal is None:
            return self

        self.clear()
        width = config.width
        height = config.height

        for cursor, code_point in self.terminal.screen.items():
            if not (0 <= cursor.x < width and 0 <= cursor.y < height):
                continue

            super().put_text(cursor.x, cursor.y, chr(code_point))

        return self

    def handle_event(self, event):
        if not super().handle_event(event):
            return False

        if isinstance(event, xproto.ExposeEvent):
            self.draw_terminal()

        return True
