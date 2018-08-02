import dataclasses
from .Reducer import Reducer

__all__ = 'init_reducers',


def init_reducers(cls):
    annotations = getattr(cls, '__annotations__', None)

    if annotations is None:
        return cls

    for name, type_hint in annotations.items():
        if issubclass(type_hint, Reducer):
            if hasattr(type_hint, 'field'):
                default = type_hint.field
            else:
                default = type_hint.reduce()
        elif dataclasses.is_dataclass(type_hint):
            default = type_hint()
        else:
            continue

        setattr(cls, name, default)

    return cls
