import functools
import os
import xcffib
from xcffib import xproto
import pyt.config


class ConnectionHandler(xcffib.Connection):
    # provides basic main loop handler
    # user of class wraps xinit and handle_event
    @classmethod
    def from_env(cls):
        display = os.getenv('DISPLAY')
        return cls(display)

    def __enter__(self):
        return self.xinit()

    def __exit__(self, exc_type, exc_value, traceback):
        super().disconnect()

    def xinit(self):
        return self

    def handle_event(self, event):
        if isinstance(event, xproto.DestroyNotifyEvent):
            return False

        return True

    def handle_next_event(self):
        super().flush()
        event = super().wait_for_event()
        return self.handle_event(event)

    def start_loop(self):
        while self.handle_next_event():
            pass

    def run(self):
        with self:
            self.start_loop()


def key_from_item(item):
    key, value = item
    return key


def parse_attrs(attrs):
    attrs_sorted = dict(sorted(attrs.items(), key=key_from_item))
    value_mask = 0

    for key in attrs_sorted.keys():
        value_mask |= key

    return value_mask, list(attrs_sorted.values())


def window_check(method):
    @functools.wraps(method)
    def wrapped(self, *args, **kwargs):
        if self.window_id is None:
            raise RuntimeError('Window has not been created')

        return method(self, *args, **kwargs)

    return wrapped


def gc_check(method):
    @functools.wraps(method)
    def wrapped(self, *args, **kwargs):
        if self.gc_id is None:
            raise RuntimeError('Graphics Context has not been created')

        return method(self, *args, **kwargs)

    return wrapped


class ConnectionAPIWrapper(ConnectionHandler):
    # Wraps core API to expose more pythonic and high level API
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.window_id = None
        self.gc_id = None

    @property
    def screen(self):
        return self.setup.roots[0]

    def create_window(self, depth, parent, x, y, width, height, border_width,
                      class_, visual, attrs):
        self.window_id = super().generate_id()
        self.core.CreateWindow(depth, self.window_id, parent, x, y, width,
                               height, border_width, class_, visual,
                               *parse_attrs(attrs))
        return self

    @window_check
    def map_window(self):
        self.core.MapWindow(self.window_id)
        return self

    @window_check
    def create_gc(self, attrs):
        self.gc_id = super().generate_id()
        self.core.CreateGC(self.gc_id, self.window_id, *parse_attrs(attrs))
        return self

    @gc_check
    def free_gc(self):
        self.core.FreeGC(self.gc_id)

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            self.free_gc()
        except RuntimeError:
            pass
        finally:
            super().__exit__(exc_type, exc_value, traceback)

    @gc_check
    @window_check
    def poly_fill_rectangle(self, *rectangles):
        self.core.PolyFillRectangle(
            self.window_id, self.gc_id, len(rectangles),
            [xproto.RECTANGLE.synthetic(*rectangle)
             for rectangle in rectangles])
        return self

    @window_check
    def change_property(self, mode, property, type, format, data,
                        data_len=None):
        if data_len is None:
            data_len = len(data)

        self.core.ChangeProperty(mode, self.window_id, property, type, format,
                                 data_len, data)
        return self

    def intern_atom(self, name, only_if_exists=False):
        return self.core\
            .InternAtom(only_if_exists, len(name), name) \
            .reply() \
            .atom


class ConnectionAbstractionLayer(ConnectionAPIWrapper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wm_delete_window = None

    def new_window(self, width, height, attrs):
        return super().create_window(
            self.screen.root_depth,
            self.screen.root,
            0, 0,  # x, y
            width, height,
            0,  # border width
            xproto.WindowClass.InputOutput,
            self.screen.root_visual,
            attrs)

    def replace_property(self, property, type, data, format=8):
        return super().change_property(
            xproto.PropMode.Replace,
            property,
            type, format,
            data)

    def set_wm_class(self, class_, instance=None):
        if instance is None:
            instance = class_

        return self.replace_property(
            xproto.Atom.WM_CLASS,
            xproto.Atom.STRING,
            f'{instance}\x00{class_}')

    def set_wm_name(self, name):
        net_wm_name = super().intern_atom('_NET_WM_NAME')
        utf8_string = super().intern_atom('UTF8_STRING')
        return self.replace_property(net_wm_name, utf8_string, name)

    def set_wm_protocols(self):
        wm_protocols = super().intern_atom('WM_PROTOCOLS')
        self.wm_delete_window = super().intern_atom('WM_DELETE_WINDOW')
        return self.replace_property(
            wm_protocols,
            xproto.Atom.ATOM,
            [self.wm_delete_window],
            format=32)

    def init_wm(self, name, class_, instance=None):
        return self \
            .set_wm_protocols() \
            .set_wm_class(class_, instance) \
            .set_wm_name(name)

    def handle_event(self, event):
        if not super().handle_event(event):
            return False

        if isinstance(event, xproto.ClientMessageEvent):
            if event.data.data32[0] == self.wm_delete_window:
                return False

        return True


class ConnectionBase(ConnectionAbstractionLayer):
    pass


class Connection(ConnectionBase):
    def xinit(self):
        return super().xinit().new_window(
            width=pyt.config.width * 6, height=pyt.config.height * 13,
            attrs={
                xproto.CW.BackPixel: self.screen.black_pixel,
                xproto.CW.EventMask: (
                    xproto.EventMask.Exposure
                    | xproto.EventMask.StructureNotify)}
        ).init_wm(
            name='Hello World XCB Example',
            class_='xcb_example',
        ).create_gc({
            xproto.GC.Foreground: self.screen.white_pixel,
            xproto.GC.GraphicsExposures: False,
        }).map_window()

    def handle_event(self, event):
        if not super().handle_event(event):
            return False

        if isinstance(event, xproto.ExposeEvent):
            self.poly_fill_rectangle((0, 0, 80 * 6, 24 * 13))

        return True


def main():
    Connection.from_env().run()


if __name__ == '__main__':
    main()
