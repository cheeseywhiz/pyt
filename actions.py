from dataclasses import dataclass
from enum import auto, Enum, Flag
import math


class StrEnum(Enum):
    # https://docs.python.org/3/library/enum.html#using-automatic-values
    def _generate_next_value_(name, start, count, last_values):
        return name


class Stack:
    @dataclass(frozen=True)
    class Push:
        pass

    @dataclass(frozen=True)
    class Pop:
        pass

    @dataclass(frozen=True)
    class Clear:
        pass


@dataclass(frozen=True)
class SetMatrix:
    xi: (int, float) = None
    yi: (int, float) = None
    ox: (int, float) = None
    xj: (int, float) = None
    yj: (int, float) = None
    oy: (int, float) = None

    @classmethod
    def update(cls, field, value):
        return cls(**{field: value})

    @classmethod
    def rotation(cls, angle_degrees):
        angle_radians = angle_degrees * math.pi / 180
        cos = math.cos(angle_radians)
        sin = math.sin(angle_radians)
        return cls(
            cos, -sin, 0,
            sin, cos, 0,
        )

    @classmethod
    def scale(cls, ratio):
        return cls(
            ratio, 0, 0,
            0, ratio, 0,
        )

    @dataclass(frozen=True)
    class Reset:
        pass


class OperationNames(StrEnum):
    DEFAULT = auto()
    ROTATION = auto()
    SCALE = auto()
    TRANSLATION = auto()
    MANUAL = auto()


@dataclass(frozen=True)
class UpdateOperation:
    operation_name: OperationNames


class GeometryOptions(Flag):
    GLOBALS = auto()
    LOCALS = auto()
    FRAMES = auto()
    INTERMEDIATE_HELPERS = auto()


@dataclass(frozen=True)
class ToggleGeometryOption:
    geometry_option: GeometryOptions


class ShapeNames(StrEnum):
    NONE = auto()
    SQUARE = auto()
    UNIT_CIRCLE = auto()
    KNOT = auto()
    FROM_JSON = auto()


class Shape:
    @dataclass(frozen=True)
    class UpdateShapeName:
        shape_name: ShapeNames

    @dataclass(frozen=True)
    class UpdateFile:
        fname: str
        data: None


class EntryOrders(StrEnum):
    GLOBAL = auto()
    LOCAL = auto()


@dataclass(frozen=True)
class UpdateEntryOrder:
    entry_order: EntryOrders
