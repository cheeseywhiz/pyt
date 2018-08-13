import dataclasses
import typing
from . import config
from . import control_codes
from .UnicodeBuffer import UnicodeBuffer
from .NextCharMode import NextCharMode
from .Tabs import Tabs

__all__ = 'TerminalBase',


@dataclasses.dataclass(frozen=True)
class FrozenBase:
    def replace(self, **changes):
        return dataclasses.replace(self, **changes)


@dataclasses.dataclass(frozen=True)
class Cursor(FrozenBase):
    x: int = 0
    y: int = 0


@dataclasses.dataclass
class TerminalBase:
    screen: typing.Dict[Cursor, int] = dataclasses.field(
        default_factory=dict,
        # repr=False,
    )
    unicode_buffer: UnicodeBuffer = UnicodeBuffer()
    next_char_mode: NextCharMode = NextCharMode.CHAR
    string_type: control_codes.C1_7B = None
    string_buffer: typing.List[int] = None
    csi_buffer: typing.List[int] = None
    cursor: Cursor = Cursor()
    set_char_set_selection: int = None
    tabs: Tabs = Tabs.from_config()

    def copy(self):
        return type(self)(
            self.screen.copy(),
            self.unicode_buffer.copy(),
            self.next_char_mode,
            self.string_type,
            None if self.string_buffer is None else self.string_buffer[:],
            None if self.csi_buffer is None else self.csi_buffer[:],
            self.cursor,
            self.set_char_set_selection,
            self.tabs.copy(),
        )

    @property
    def next_tab(self):
        if self.cursor.x == config.width - 1:
            return config.width - 1

        return self.tabs.next_tab(self.cursor.x)
