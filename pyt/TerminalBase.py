import dataclasses
import typing
from . import control_codes
from .UnicodeBuffer import UnicodeBuffer
from .NextCharMode import NextCharMode

__all__ = 'TerminalBase',


CursorT = typing.Tuple[int, int]


@dataclasses.dataclass
class TerminalBase:
    screen: typing.Dict[CursorT, int] = dataclasses.field(
        default_factory=dict, repr=False,
    )
    unicode_buffer: UnicodeBuffer = UnicodeBuffer()
    next_char_mode: NextCharMode = NextCharMode.CHAR
    string_type: control_codes.C1_7B = None
    string_buffer: typing.List[int] = None
    csi_buffer: typing.List[int] = None
    cursor: CursorT = (0, 0)
    set_char_set_selection: int = None

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
        )
