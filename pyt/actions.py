import dataclasses
import typing

__all__ = 'PutByte', 'PutByteSequence', 'PutCodePoint', 'PutString'


@dataclasses.dataclass(frozen=True)
class PutByte:
    byte: int


@dataclasses.dataclass(frozen=True)
class PutByteSequence:
    byte_sequence: typing.List[int]


@dataclasses.dataclass(frozen=True)
class PutCodePoint:
    code_point: int


@dataclasses.dataclass(frozen=True)
class PutString:
    string: str
