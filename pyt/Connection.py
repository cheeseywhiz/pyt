from xcffib import xproto
from .ConnectionBase import ConnectionBase
from . import config

__all__ = 'Connection',


class Connection(ConnectionBase):
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

    def handle_event(self, event):
        if not super().handle_event(event):
            return False

        if isinstance(event, xproto.ExposeEvent):
            width = 80
            height = 24
            width *= self.font_info.width
            height *= self.font_info.height
            width //= 3
            height //= 3
            super().poly_fill_rectangle(
                (0, 0, width, height),
                (0, 2 * height, width, height),
                (2 * width, 0, width, height),
                (2 * width, 2 * height, width, height),
            ).put_text(
                1, 1, 'hello world',
            ).put_text(
                1, 3, 'goodbye world',
            )

        return True
