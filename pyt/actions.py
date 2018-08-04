import dataclasses


@dataclasses.dataclass(frozen=True)
class PutChar:
    char: str


@dataclasses.dataclass(frozen=True)
class PutString:
    string: str
