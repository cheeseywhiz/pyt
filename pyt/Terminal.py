import dataclasses
import typing
import redux
from . import actions

__all__ = 'Terminal',


class Lines(redux.Reducer[typing.List[str]]):
    field = dataclasses.field(
        default_factory=lambda: [''],
    )

    def reduce(state=None, action=None):
        if isinstance(action, actions.PutChar):
            new_state = state[:]
            new_state[-1] += action.char
            return new_state

        return state


@dataclasses.dataclass(frozen=True)
@redux.init_reducers
class Terminal(redux.CombineReducers):
    lines_hint: Lines
