import dataclasses
import actions
import Reducer
from CombineReducers import CombineReducers
from init_reducers import init_reducers

__all__ = 'CombineReducersStack',


class Stack(Reducer.Reducer[list]):
    field = dataclasses.field(default_factory=list)

    def reduce(state=None, action=None):
        if state is None or isinstance(action, actions.Stack.Clear):
            state = []

        return state


@dataclasses.dataclass(frozen=True)
@init_reducers
class CombineReducersStackBase(CombineReducers):
    stack: Stack

    def stack_update(self, action=None):
        if isinstance(action, actions.Stack.Push):
            entry = self._stack_entry(**vars(self))
            return {'stack': [*self.stack, entry]}
        elif isinstance(action, actions.Stack.Pop):
            if not self.stack:
                return self

            *stack, entry = self.stack
            return {'stack': stack, **vars(entry)}

        return self

    def reduce(self, action=None):
        new_data = super().reduce(action)
        stack_update = self.stack_update(action)

        if stack_update is self:
            return new_data

        new_dict = vars(new_data).copy()
        new_dict.update(stack_update)
        return type(self)(**new_dict)


class IgnoreStackMixin:
    def __init__(self, *args, **kwargs):
        kwargs.pop('stack', None)
        super().__init__(*args, **kwargs)


class CombineReducersStackMeta(type):
    def __new__(cls, name, bases, namespace):
        self = super().__new__(cls, name, bases, namespace)
        new_namespace = namespace.copy()
        new_namespace['__qualname__'] += 'EntryBase'
        stack_entry_base = super().__new__(
            cls, name + 'EntryBase', (), new_namespace,
        )
        stack_entry_base = init_reducers(stack_entry_base)
        stack_entry_base = dataclasses.dataclass(stack_entry_base, frozen=True)
        self._stack_entry = super().__new__(
            cls, name + 'Entry', (IgnoreStackMixin, stack_entry_base), {},
        )
        return self


class CombineReducersStack(
        CombineReducersStackBase, metaclass=CombineReducersStackMeta,
):
    pass
