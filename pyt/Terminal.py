import dataclasses
import typing
import enum
from . import actions
from . import control_codes
from .ParsedCSI import ParsedCSI

__all__ = 'Terminal',


def empty_matrix(rows, columns, obj=None):
    row = [obj] * columns
    return [row[:] for _ in range(rows)]


class StrEnum(enum.Enum):
    # https://docs.python.org/3/library/enum.html#using-automatic-values
    def _generate_next_value_(name, start, count, last_values):
        return name


class NextCharMode(StrEnum):
    CHAR = enum.auto()
    ESC = enum.auto()
    CSI = enum.auto()
    STRING = enum.auto()
    STRING_ESC = enum.auto()


CursorT = typing.Tuple[int, int]


@dataclasses.dataclass
class Terminal:
    screen: typing.Dict[CursorT, str] = dataclasses.field(
        default_factory=dict, repr=False,
    )
    next_char_mode: NextCharMode = NextCharMode.CHAR
    string_type: control_codes.C1_7B = None
    string_buffer: typing.List[str] = None
    csi_buffer: typing.List[str] = None
    cursor: CursorT = (0, 0)

    def copy(self):
        return type(self)(
            self.screen.copy(),
            self.next_char_mode,
            self.string_type,
            None if self.string_buffer is None else self.string_buffer[:],
            None if self.csi_buffer is None else self.csi_buffer[:],
            self.cursor,
        )

    def cursor_up(self, n_lines=None):
        if n_lines is None:
            n_lines = 1

        x, y = self.cursor
        self.cursor = x, y - n_lines
        return self

    def cursor_down(self, n_lines=None):
        if n_lines is None:
            n_lines = 1

        x, y = self.cursor
        self.cursor = x, y + n_lines
        return self

    def cursor_forward(self, n_cols=None):
        if n_cols is None:
            n_cols = 1

        x, y = self.cursor
        self.cursor = x + n_cols, y
        return self

    def cursor_backward(self, n_cols=None):
        if n_cols is None:
            n_cols = 1

        x, y = self.cursor
        self.cursor = x - n_cols, y
        return self

    def cursor_character_absolute(self, nth_col=None):
        if nth_col is None:
            nth_col = 1

        x, y = self.cursor
        self.cursor = nth_col - 1, y
        return self

    def cursor_next_line(self, n_lines=None):
        return self \
            .carriage_return() \
            .cursor_down(n_lines)

    def cursor_preceding_line(self, n_lines=None):
        return self \
            .carriage_return() \
            .cursor_up(n_lines)

    def cursor_position(self, nth_line=None, nth_col=None):
        if nth_line is None:
            nth_line = 1

        if nth_col is None:
            nth_col = 1

        self.cursor = nth_col - 1, nth_line - 1
        return self

    def backspace(self):
        return self.cursor_backward()

    def carriage_return(self):
        return self.cursor_character_absolute()

    def line_feed(self):
        return self.cursor_next_line()

    def add_char(self, char):
        self.screen[self.cursor] = char
        return self.cursor_forward()

    def reset(self):
        return type(self)()

    def reset_string_buffer(self, string_type=None):
        self.string_buffer = []
        self.string_type = string_type
        return self

    def reset_csi_buffer(self):
        self.csi_buffer = []
        return self

    def handle_C0(self, C0):
        if C0 is control_codes.C0.BS:
            return self.backspace()
        if C0 in (
                control_codes.C0.LF,
                control_codes.C0.VT,
                control_codes.C0.FF,
        ):
            return self.line_feed()
        elif C0 is control_codes.C0.CR:
            return self.carriage_return()
        elif C0 is control_codes.C0.ESC:
            self.next_char_mode = NextCharMode.ESC
            return self

        print(f'Unhandled C0: {C0 !r}')
        return self

    def handle_C1(self, C1):
        self.next_char_mode = NextCharMode.CHAR

        if C1 is control_codes.C1_7B.CSI:
            self.next_char_mode = NextCharMode.CSI
            return self.reset_csi_buffer()
        elif C1 in (
                control_codes.C1_7B.APC,
                control_codes.C1_7B.DCS,
                control_codes.C1_7B.OSC,
                control_codes.C1_7B.PM,
                control_codes.C1_7B.SOS,
        ):
            self.next_char_mode = NextCharMode.STRING
            return self.reset_string_buffer(C1)
        elif C1 is control_codes.C1_7B.NEL:
            return self.add_newline()
        elif C1 is control_codes.C1_7B.RIS:
            return self.reset()

        print(f'Unhandled C1: {C1 !r}')
        return self

    def handle_char(self, char):
        code_point = ord(char)
        C0 = control_codes.C0(code_point)

        if C0 is not None:
            return self.handle_C0(C0)

        return self.add_char(char)

    def handle_esc(self, char):
        code_point = ord(char)
        C1 = control_codes.C1_7B(code_point)

        if C1 is not None:
            return self.handle_C1(C1)

        print(f'Unknown esc: %s' % hex(ord(char)))
        self.next_char_mode = NextCharMode.CHAR
        return self

    def do_csi(self, csi):
        if csi.csi_type is control_codes.CSI.CUU:
            return self.cursor_up(*csi.args)
        elif csi.csi_type is control_codes.CSI.CUD:
            return self.cursor_down(*csi.args)
        elif csi.csi_type is control_codes.CSI.CUF:
            return self.cursor_forward(*csi.args)
        elif csi.csi_type is control_codes.CSI.CUB:
            return self.cursor_backward(*csi.args)
        elif csi.csi_type is control_codes.CSI.CNL:
            return self.cursor_next_line(*csi.args)
        elif csi.csi_type is control_codes.CSI.CPL:
            return self.cursor_preceding_line(*csi.args)
        elif csi.csi_type is control_codes.CSI.CHA:
            return self.cursor_character_absolute(*csi.args)
        elif csi.csi_type is control_codes.CSI.CUP:
            return self.cursor_position(*csi.args)

        print(f'Unhandled csi: {csi}')
        return self

    def parse_csi(self):
        self.next_char_mode = NextCharMode.CHAR
        csi_string = ''.join(self.csi_buffer[:-1])
        final_byte = control_codes.CSI(ord(self.csi_buffer[-1]))
        csi = ParsedCSI(final_byte, csi_string)
        return self \
            .reset_csi_buffer() \
            .do_csi(csi)

    def handle_csi(self, char):
        code_point = ord(char)

        if code_point in range(0x20, 0x30):
            print('Ignoring intermediate byte (%s)' % hex(code_point))

        final_byte = control_codes.CSI(code_point)

        if final_byte is not None or code_point in range(0x30, 0x40):
            self.csi_buffer.append(char)

            if final_byte is not None:
                return self.parse_csi()

            return self

        print(f'Unknown csi: %s' % hex(ord(char)))
        return self

    def parse_string_impl(self, string_type, string):
        print(f'Received string ({string_type !r}) {string !r}')
        return self

    def parse_string(self):
        self.next_char_mode = NextCharMode.CHAR
        string_type = self.string_type
        string = ''.join(self.string_buffer)
        return self \
            .reset_string_buffer() \
            .parse_string_impl(string_type, string)

    def handle_string_C0(self, C0):
        if C0 is control_codes.C0.BEL:
            return self.parse_string()
        elif C0 is control_codes.C0.ESC:
            self.next_char_mode = NextCharMode.STRING_ESC
            return self

        return self

    def handle_string(self, char):
        code_point = ord(char)
        C0 = control_codes.C0(code_point)

        if C0 is not None:
            return self.handle_string_C0(C0)

        self.string_buffer.append(char)
        return self

    def handle_string_esc(self, char):
        code_point = ord(char)

        if control_codes.C1_7B(code_point) is control_codes.C1_7B.ST:
            return self.parse_string()
        else:
            # string interrupted
            self.next_char_mode = NextCharMode.ESC
            return self \
                .reset_string_buffer() \
                .handle_esc()

    @property
    def put_char_func(self):
        return {
            NextCharMode.CHAR: self.handle_char,
            NextCharMode.ESC: self.handle_esc,
            NextCharMode.CSI: self.handle_csi,
            NextCharMode.STRING: self.handle_string,
            NextCharMode.STRING_ESC: self.handle_string_esc,
        }[self.next_char_mode]

    def put_char(self, char):
        return self.put_char_func(char)

    def put_string(self, string):
        self_chain = self

        for char in string:
            self_chain = self_chain.put_char(char)

        return self_chain

    @property
    def screen_str(self):
        width = 227
        height = 56
        screen = empty_matrix(height, width, ' ')

        for (x, y), char in self.screen.items():
            if x >= width or y >= height:
                continue

            screen[y][x] = char

        return '\n'.join(''.join(row) for row in screen)

    def reduce(self, action=None):
        if isinstance(action, actions.PutChar):
            return self.copy().put_char(action.char)
        if isinstance(action, actions.PutString):
            return self.copy().put_string(action.string)

        return self
