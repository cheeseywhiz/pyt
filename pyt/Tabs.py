import collections.abc
import pyt

__all__ = 'Tabs',


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
        return f'{qualname}({list(self) !r})'


class Tabs(MutableSet):
    @classmethod
    def from_config(cls, *, width=None, tab_width=None):
        if width is None:
            width = pyt.config.width

        if tab_width is None:
            tab_width = pyt.config.tab_width

        self = cls(range(0, width, tab_width))
        self.add(width - 1)
        return self

    def __iter__(self):
        return iter(sorted(super().__iter__()))

    def next_tab(self, after):
        for tab in self:
            if after < tab:
                return tab
