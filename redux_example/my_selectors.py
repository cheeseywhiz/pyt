import numpy as np
import redux
import actions
from State import Stack


def matrix(state):
    return state.matrix


@redux.selector(matrix)
def number(matrix):
    return matrix.number


@redux.selector(matrix)
def frame(matrix):
    return np.array([
        [matrix.xi or 1, matrix.yi or 0, matrix.ox or 0, ],
        [matrix.xj or 0, matrix.yj or 1, matrix.oy or 0, ],
        [0, 0, 1],
    ], dtype=float)


def operation(state):
    return state.operation


def geometry(state):
    return state.geometry


def entry_order(state):
    return state.entry_order


def shape(state):
    return state.shape


class Shape:
    @redux.selector(shape)
    def shape_name(shape):
        return shape.shape_name

    @redux.selector(shape)
    def file(shape):
        return shape.file


@redux.selector(lambda state: state.stack)
def stack(stack):
    return [
        state
        for state in stack
        if not matrix(state).is_identity()
    ]


@redux.selector(stack, matrix, operation, entry_order)
def full(stack, matrix, operation, entry_order):
    full = stack[:]
    entry = Stack._stack_entry(matrix, operation)

    if not matrix.is_identity():
        full.append(entry)

    if entry_order == actions.EntryOrders.LOCAL:
        full = list(reversed(full))

    return full


@redux.selector(full)
def globals_(full):
    frames = map(frame, full)
    globals_ = [np.eye(3)]

    for frame_ in frames:
        globals_.append(frame_ @ globals_[-1])

    return globals_


@redux.selector(full)
def locals_(full):
    frames = reversed(map(frame, full))
    locals_ = [np.eye(3)]

    for frame_ in frames:
        globals_.append(locals_[-1] @ frame_)
