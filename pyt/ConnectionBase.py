import dataclasses
import functools
import xcffib
from xcffib import xproto
import pyt.config
from .ConnectionHandler import ConnectionHandler


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


def font_check(method):
    @functools.wraps(method)
    def wrapped(self, *args, **kwargs):
        if self.font_id is None:
            raise RuntimeError('Font has not been opened')

        return method(self, *args, **kwargs)

    return wrapped


class ConnectionAPIWrapper(ConnectionHandler):
    # Wraps core API to expose more pythonic and high level API
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.window_id = None
        self.gc_id = None
        self.font_id = None

    @property
    def screen(self):
        return self.setup.roots[0]

    @staticmethod
    def parse_attrs(attrs):
        def key_from_item(item):
            key, value = item
            return key

        attrs_sorted = dict(sorted(attrs.items(), key=key_from_item))
        value_mask = 0

        for key in attrs_sorted.keys():
            value_mask |= key

        return value_mask, list(attrs_sorted.values())

    def create_window(self, depth, parent, x, y, width, height, border_width,
                      class_, visual, attrs=None):
        if attrs is None:
            attrs = {}

        self.window_id = super().generate_id()
        self.core.CreateWindow(depth, self.window_id, parent, x, y, width,
                               height, border_width, class_, visual,
                               *self.parse_attrs(attrs))
        return self

    @window_check
    def map_window(self):
        self.core.MapWindow(self.window_id)
        return self

    @window_check
    def create_gc(self, attrs=None):
        if attrs is None:
            attrs = {}

        self.gc_id = super().generate_id()
        self.core.CreateGC(self.gc_id, self.window_id,
                           *self.parse_attrs(attrs))
        return self

    @gc_check
    def free_gc(self):
        self.core.FreeGC(self.gc_id)
        self.gc_id = None
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.gc_id:
            self.free_gc()

        if self.font_id:
            self.close_font()

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

    def open_font(self, name):
        try:
            self.close_font()
        except RuntimeError:
            self.font_id = super().generate_id()
            self.core.OpenFont(self.font_id, len(name), name)
        finally:
            return self

    @font_check
    def close_font(self):
        self.core.CloseFont(self.font_id)
        self.font_id = None
        return self

    @gc_check
    def image_text_8(self, x, y, text):
        self.core.ImageText8(len(text), self.window_id, self.gc_id, x, y, text)
        return self

    @font_check
    def query_font(self):
        return self.core.QueryFont(self.font_id).reply()

    @window_check
    def clear_area(self, x, y, width, height, exposures=True):
        self.core.ClearArea(exposures, self.window_id, x, y, width, height)
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

    def new_window(self, width, height, attrs=None):
        return super().create_window(
            self.screen.root_depth,
            self.screen.root,
            0, 0,  # x, y
            width, height,
            0,  # border width
            xproto.WindowClass.InputOutput,
            self.screen.root_visual,
            attrs=attrs)

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

    def init_wm(self, class_, name=None, instance=None):
        if name is None:
            name = class_

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

    def clear(self):
        return super().clear_area(0, 0, 0xffff, 0xffff, exposures=False)


@dataclasses.dataclass
class FontOffset:
    left: int = 0
    ascent: int = 0

    @classmethod
    def from_font_query(cls, font_query):
        return cls(
            font_query.min_bounds.left_side_bearing,
            font_query.max_bounds.ascent)

    def apply_to_xy(self, x, y):
        return x - self.left, y + self.ascent


@dataclasses.dataclass
class FontInfo:
    width: int = 1
    height: int = 1
    offset: FontOffset = dataclasses.field(default_factory=FontOffset)

    @classmethod
    def from_font_query(cls, font_query):
        max_bounds = font_query.max_bounds
        min_bounds = font_query.min_bounds
        return cls(
            max_bounds.right_side_bearing - min_bounds.left_side_bearing,
            max_bounds.ascent + max_bounds.descent,
            FontOffset.from_font_query(font_query))

    def cell_to_xy(self, row, col):
        return self.offset.apply_to_xy(row * self.width, col * self.height)


class ConnectionFont(ConnectionAbstractionLayer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.font_info = FontInfo()

    def init_font(self, name):
        font_query = super().open_font(name).query_font()
        self.font_info = FontInfo.from_font_query(font_query)
        return self

    def put_text(self, row, col, text):
        return super().image_text_8(*self.font_info.cell_to_xy(row, col), text)

    def new_window(self, n_rows, n_cols, attrs=None):
        width = n_cols * self.font_info.width
        height = n_rows * self.font_info.height
        return super().new_window(width, height, attrs=attrs)


class ConnectionBase(ConnectionFont):
    pass
