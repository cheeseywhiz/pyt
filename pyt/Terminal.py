import dataclasses
import typing
import redux
from . import actions
from . import control_codes

__all__ = 'Terminal',


@dataclasses.dataclass(frozen=True)
class Terminal(redux.CombineReducers):
    lines: typing.List[str] = dataclasses.field(
        default_factory=lambda: [''],
    )

    def copy(self):
        return type(self)(self.lines[:])

    def add_char(self, char):
        self.lines[-1] += char
        return self

    def add_C0(self, C0):
        if C0 in (
                control_codes.C0.LF,
                control_codes.C0.VT,
                control_codes.C0.FF,
        ):
            self.lines.append('')

        return self

    def put_char(self, char):
        code_point = ord(char)

        if code_point in control_codes.C0:
            C0 = control_codes.C0(code_point)
            return self.add_C0(C0)

        return self.add_char(char)

    def reduce(self, action=None):
        if isinstance(action, actions.PutChar):
            return self.copy().put_char(action.char)

        return self
