import enum

__all__ = 'NextCharMode'


class StrEnum(enum.Enum):
    # https://docs.python.org/3/library/enum.html#using-automatic-values
    def _generate_next_value_(name, start, count, last_values):
        return name


class NextCharMode(StrEnum):
    CHAR = enum.auto()
    ESC = enum.auto()
    CSI = enum.auto()
    STRING = enum.auto()
    STRING_ESC = enum.auto()
    SET_CHAR_SET = enum.auto()
