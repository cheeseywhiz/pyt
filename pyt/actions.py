import dataclasses


@dataclasses.dataclass(frozen=True)
class PutChar:
    char: str
