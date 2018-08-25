from xcffib import xproto
from .ConnectionBase import ConnectionBase
from . import config
from .Terminal import Terminal

__all__ = 'Connection',


class Connection(ConnectionBase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.terminal = None

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

    def draw_terminal(self):
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

        if isinstance(event, Terminal):
            self.terminal = event
            self.draw_terminal()

        return True
