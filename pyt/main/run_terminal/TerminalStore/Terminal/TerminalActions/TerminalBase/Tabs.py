import collections.abc
from ....... import config

__all__ = 'Tabs'


class MutableSet(collections.abc.MutableSet):
    __slots__ = '__set',

    def __init__(self, *args, **kwargs):
        self.__set = set(*args, **kwargs)

    def __contains__(self, item):
        return item in self.__set

    def __iter__(self):
        return iter(self.__set)

    def __len__(self):
        return len(self.__set)

    def add(self, item):
        self.__set.add(item)

    def discard(self, item):
        self.__set.discard(item)

    def copy(self):
        return type(self)(self)

    def __repr__(self):
        qualname = self.__class__.__qualname__
        return f'{qualname}({sorted(self) !r})'


class Tabs(MutableSet):
    @classmethod
    def from_config(cls, *, width=None, tab_width=None):
        if width is None:
            width = config.width

        if tab_width is None:
            tab_width = config.tab_width

        return cls(range(0, width, tab_width))

    def next_tabs(self, after):
        return sorted(filter(lambda tab: tab > after, self))
