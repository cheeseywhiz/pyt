import dataclasses
import typing
from . import control_codes

__all__ = 'ParsedCSI'


@dataclasses.dataclass
class ParsedCSIBase:
    csi_type: control_codes.CSI
    private: bool
    args: typing.List[typing.Union[int, float, None]]


class ParsedCSI(ParsedCSIBase):
    def __init__(self, csi_type, csi_string):
        if not csi_string:
            super().__init__(csi_type, False, [])
            return

        private = ord(csi_string[0]) in range(0x3c, 0x40)

        if private:
            csi_string = csi_string[1:]

        args = []

        for arg in csi_string.split(';'):
            if arg != '0':
                arg = arg.lstrip('0')

            if ':' in arg:
                arg = float(arg.replace(':', '.'))
            elif arg:
                arg = int(arg)
            else:
                arg = None

            args.append(arg)

        super().__init__(csi_type, private, args)
