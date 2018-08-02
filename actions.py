import dataclasses
import enum
import math


class StrEnum(enum.Enum):
    # https://docs.python.org/3/library/enum.html#using-automatic-values
    def _generate_next_value_(name, start, count, last_values):
        return name


class Stack:
    @dataclasses.dataclass(frozen=True)
    class Push:
        pass

    @dataclasses.dataclass(frozen=True)
    class Pop:
        pass

    @dataclasses.dataclass(frozen=True)
    class Clear:
        pass


@dataclasses.dataclass(frozen=True)
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

    @dataclasses.dataclass(frozen=True)
    class Reset:
        pass


class OperationNames(StrEnum):
    DEFAULT = enum.auto()
    ROTATION = enum.auto()
    SCALE = enum.auto()
    TRANSLATION = enum.auto()
    MANUAL = enum.auto()


@dataclasses.dataclass(frozen=True)
class UpdateOperation:
    operation_name: OperationNames


class GeometryOptions(enum.Flag):
    GLOBALS = enum.auto()
    LOCALS = enum.auto()
    FRAMES = enum.auto()
    INTERMEDIATE_HELPERS = enum.auto()


@dataclasses.dataclass(frozen=True)
class ToggleGeometryOption:
    geometry_option: GeometryOptions


class ShapeNames(StrEnum):
    NONE = enum.auto()
    SQUARE = enum.auto()
    UNIT_CIRCLE = enum.auto()
    KNOT = enum.auto()
    FROM_JSON = enum.auto()


class Shape:
    @dataclasses.dataclass(frozen=True)
    class UpdateShapeName:
        shape_name: ShapeNames

    @dataclasses.dataclass(frozen=True)
    class UpdateFile:
        fname: str
        data: None


class EntryOrders(StrEnum):
    GLOBAL = enum.auto()
    LOCAL = enum.auto()


@dataclasses.dataclass(frozen=True)
class UpdateEntryOrder:
    entry_order: EntryOrders
