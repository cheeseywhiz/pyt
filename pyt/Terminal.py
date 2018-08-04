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
    lines: typing.List[str] = dataclasses.field(
        default_factory=lambda: [''],
    )
    next_char_mode: NextCharMode = NextCharMode.CHAR

    def copy(self):
        return type(self)(
            self.lines[:],
            self.next_char_mode,
        )

    def add_char(self, char):
        self.lines[-1] += char
        return self

    def add_newline(self):
        self.lines.append('')
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
            return self
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

        print('Unknown string: %s' % hex(ord(char)))
        return self

    def handle_string_esc(self, char):
        code_point = ord(char)

        if control_codes.C1_7B(code_point) is control_codes.C1_7B.ST:
            return self.parse_string()
        else:
            # string interrupted
            # TODO: reset string buffer
            self.next_char_mode = NextCharMode.ESC
            return self.handle_esc(char)

    def put_char(self, char):
        if self.next_char_mode is NextCharMode.CHAR:
            return self.handle_char(char)
        elif self.next_char_mode is NextCharMode.ESC:
            return self.handle_esc(char)
        elif self.next_char_mode is NextCharMode.CSI:
            return self.handle_csi(char)
        elif self.next_char_mode is NextCharMode.STRING:
            return self.handle_string(char)
        elif self.next_char_mode is NextCharMode.STRING_ESC:
            return self.handle_string_esc(char)

        return self

    def put_string(self, string):
        self_chain = self

        for char in string:
            self_chain = self_chain.put_char(char)

        return self_chain

    def reduce(self, action=None):
        if isinstance(action, actions.PutChar):
            return self.copy().put_char(action.char)
        if isinstance(action, actions.PutString):
            return self.copy().put_string(action.string)

        return self
