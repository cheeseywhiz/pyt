import dataclasses
import typing

__all__ = 'Reducer',


StateT = typing.TypeVar('StateT')


@dataclasses.dataclass
class Reducer(typing.Generic[StateT]):
    field: StateT

    @staticmethod
    def reduce(state: StateT, action: typing.Any=None) -> StateT:
        raise TypeError('Reducer subclass must implement reduce method')
