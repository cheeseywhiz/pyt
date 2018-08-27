import dataclasses
import typing

__all__ = (
    'PutByte', 'PutByteSequence', 'PutCodePoint', 'PutString', 'KeyboardInput',
    'Quit',
)

action = dataclasses.dataclass(frozen=True)


@action
class PutByte:
    byte: int


@action
class PutByteSequence:
    byte_sequence: typing.List[int]


@action
class PutCodePoint:
    code_point: int


@action
class PutString:
    string: str


@action
class KeyboardInput:
    keyboard_input: str


@action
class Quit:
    pass
