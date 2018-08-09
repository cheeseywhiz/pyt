import dataclasses

__all__ = 'PutCodePoint', 'PutString'


@dataclasses.dataclass(frozen=True)
class PutCodePoint:
    code_point: int


@dataclasses.dataclass(frozen=True)
class PutString:
    string: str
