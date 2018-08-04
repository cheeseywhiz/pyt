import dataclasses
import typing
import redux
from . import actions
from . import control_codes

__all__ = 'Terminal',


class Lines(redux.Reducer[typing.List[str]]):
    field = dataclasses.field(
        default_factory=lambda: [''],
    )

    def add_char(state, char):
        state[-1] += char
        return state

    def add_C0(state, C0):
        if C0 in (
                control_codes.C0.LF,
                control_codes.C0.VT,
                control_codes.C0.FF,
        ):
            state.append('')

        return state

    def put_char(state, char):
        code_point = ord(char)

        if code_point in control_codes.C0:
            C0 = control_codes.C0(code_point)
            return Lines.add_C0(state, C0)

        return Lines.add_char(state, char)

    def reduce(state=None, action=None):
        if isinstance(action, actions.PutChar):
            return Lines.put_char(state[:], action.char)

        return state


@dataclasses.dataclass(frozen=True)
@redux.init_reducers
class Terminal(redux.CombineReducers):
    lines: Lines
