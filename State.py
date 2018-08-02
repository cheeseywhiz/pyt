import dataclasses
import typing
import actions
from Reducer import Reducer
from init_reducers import init_reducers
from CombineReducers import CombineReducers
from CombineReducersStack import CombineReducersStack
from MergeReducers import MergeReducers

__all__ = 'State',


@dataclasses.dataclass(frozen=True)
class Matrix:
    xi: typing.Union[int, float] = 1
    yi: typing.Union[int, float] = 0
    ox: typing.Union[int, float] = 0
    xj: typing.Union[int, float] = 0
    yj: typing.Union[int, float] = 1
    oy: typing.Union[int, float] = 0

    def merge(self, other):
        kwargs = {}

        for data in (self, other):
            kwargs.update(vars(data))

        return type(self)(**kwargs)

    def reduce(self, action=None):
        if isinstance(action, actions.SetMatrix):
            return self.merge(action)
        elif isinstance(action, (
                actions.UpdateOperation,
                actions.Stack.Push,
                actions.SetMatrix.Reset
        )):
            return type(self)()

        return self


class Operation(Reducer[actions.OperationNames]):
    def reduce(state=None, action=None):
        if state is None:
            state = actions.OperationNames.DEFAULT

        if isinstance(action, actions.UpdateOperation):
            return action.operation_name

        return state


class Geometry(Reducer[actions.GeometryOptions]):
    def reduce(state=None, action=None):
        if state is None:
            state = actions.GeometryOptions.FRAMES

        if isinstance(action, actions.ToggleGeometryOption):
            return state ^ action.geometry_option

        return state


class EntryOrder(Reducer[actions.EntryOrders]):
    def reduce(state=None, action=None):
        if state is None:
            state = actions.EntryOrders.GLOBAL

        if isinstance(action, actions.UpdateEntryOrder):
            return action.entry_order

        return state


class ShapeName(Reducer[actions.ShapeNames]):
    def reduce(state=None, action=None):
        if state is None:
            state = actions.ShapeNames.NONE

        if isinstance(action, actions.Shape.UpdateShapeName):
            return action.shape_name

        return state


@dataclasses.dataclass(frozen=True)
class File:
    fname: str = None
    data: typing.Any = None

    def reduce(self, action=None):
        if isinstance(action, actions.Shape.UpdateFile):
            return type(self)(action.fname, action.data)

        return self


@dataclasses.dataclass(frozen=True)
@init_reducers
class Shape(CombineReducers):
    shape_name: ShapeName
    file: File


class State(MergeReducers):
    @dataclasses.dataclass(frozen=True)
    @init_reducers
    class Stack(CombineReducersStack):
        matrix: Matrix
        operation: Operation

    @dataclasses.dataclass(frozen=True)
    @init_reducers
    class StateBase(CombineReducers):
        geometry: Geometry
        entry_order: EntryOrder
        shape: Shape
