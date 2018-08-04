import dataclasses
import typing
import enum
import redux
from . import actions
from . import control_codes

__all__ = 'Terminal',


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


@dataclasses.dataclass
class Terminal(redux.CombineReducers):
    lines: typing.List[typing.List[str]] = dataclasses.field(
        default_factory=lambda: [[]],
    )
    next_char_mode: NextCharMode = NextCharMode.CHAR
    string_type: control_codes.C1_7B = None
    string_buffer: typing.List[str] = dataclasses.field(
        default_factory=list,
    )

    def copy(self):
        return type(self)(
            self.lines[:],
            self.next_char_mode,
            self.string_type,
            self.string_buffer[:],
        )

    def add_char(self, char):
        self.lines[-1].append(char)
        return self

    def add_newline(self):
        self.lines.append([])
        return self

    def reset_string_buffer(self, string_type=None):
        self.string_buffer = []

        if string_type is not None:
            self.string_type = string_type

        return self

    def handle_C0(self, C0):
        if C0 in (
                control_codes.C0.LF,
                control_codes.C0.VT,
                control_codes.C0.FF,
        ):
            return self.add_newline()
        elif C0 is control_codes.C0.ESC:
            self.next_char_mode = NextCharMode.ESC
            return self

        print(f'Unknown C0: {C0 !r}')
        return self

    def handle_C1(self, C1):
        self.next_char_mode = NextCharMode.CHAR

        if C1 is control_codes.C1_7B.CSI:
            self.next_char_mode = NextCharMode.CSI
            return self
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

        print(f'Unknown C1: {C1 !r}')
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

    def handle_csi(self, char):
        code_point = ord(char)
        final_byte = control_codes.CSI(code_point)

        if final_byte is not None:
            self.next_char_mode = NextCharMode.CHAR
            print(f'Unknown final csi: {final_byte !r}')
            return self
        elif code_point in range(0x20, 0x30):
            intermediate_byte = code_point
            print(f'Unknown intermediate csi: %s' % hex(ord(char)))
            return self
        elif code_point in range(0x30, 0x40):
            parameter_byte = code_point
            print(f'Unknown parameter csi: %s' % hex(ord(char)))
            return self

        print(f'Unknown csi: %s' % hex(ord(char)))
        return self

    def parse_string(self):
        self.next_char_mode = NextCharMode.CHAR
        string = ''.join(self.string_buffer)
        self.reset_string_buffer()
        print(f'Received string ({self.string_type !r}) {string !r}')
        return self

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
    def screen(self):
        return '\n'.join(''.join(row) for row in self.lines)

    def reduce(self, action=None):
        if isinstance(action, actions.PutChar):
            return self.copy().put_char(action.char)
        if isinstance(action, actions.PutString):
            return self.copy().put_string(action.string)

        return self
