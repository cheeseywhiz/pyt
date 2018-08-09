import dataclasses
import typing

__all__ = 'UnicodeBuffer',


def get_n_bytes(first):
    if first in range(0x80):
        return 1
    elif first in range(0xc2, 0xe0):
        return 2
    elif first in range(0xe0, 0xf0):
        return 3
    elif first in range(0xf0, 0xf5):
        return 4
    else:
        return 0


def verify_n_bytes(unicode_bytes):
    n_bytes = get_n_bytes(unicode_bytes[0])

    if n_bytes == 0 or len(unicode_bytes) != n_bytes:
        return 0

    return n_bytes


def verify_unicode_bytes(first=None, second=None, third=None, fourth=None):
    if fourth:
        return fourth in range(0x80, 0xc0) and third in range(0x80, 0xc0) and (
            (second in range(0x90, 0xc0) and first == 0xf0)
            or (second in range(0x80, 0xc0) and first in range(0xf1, 0xf4))
            or (second in range(0x80, 0x90) and first == 0xf4)
        )

    if third:
        return third in range(0x80, 0xc0) and (
            (second in range(0x80, 0xc0) and (first in range(0xe1, 0xed) or
                                              first in range(0xee, 0xf0)))
            or (second in range(0xa0, 0xc0) and first == 0xe0)
            or (second in range(0x80, 0xa0) and first == 0xed)
        )

    if second:
        return first in range(0xc2, 0xe0) and second in range(0x80, 0xc0)

    if first:
        return True


def verify(unicode_bytes):
    return verify_n_bytes(unicode_bytes) \
        and verify_unicode_bytes(*unicode_bytes)


def decode_verified(first=None, second=None, third=None, fourth=None):
    if fourth:
        xx = fourth & 0b00111111
        yy = (third & 0b00111111) << 6
        zz = (second & 0b00001111) << 12
        uu = (
            ((first & 0b00000111) << 2) | ((second & 0b00110000) >> 4)
        ) << 16
        return uu | zz | yy | xx

    if third:
        xx = third & 0b00111111
        yy = (second & 0b00111111) << 6
        zz = (first & 0b00001111) << 12
        return zz | yy | xx

    if second:
        xx = second & 0b00111111
        yy = (first & 0b00011111) << 6
        return yy | xx

    if first:
        return first


def decode(unicode_bytes):
    if verify(unicode_bytes):
        return decode_verified(*unicode_bytes)
    else:
        raise UnicodeError


def encode(code_point):
    xx = code_point & 0b00000000_00111111
    yy = (code_point & 0b00001111_11000000) >> 6
    zz = (code_point & 0b11110000_00000000) >> 12
    uu = (code_point & 0b00011111_00000000_00000000) >> 16

    x_byte = 0b10000000 | xx
    y_byte = 0b10000000 | yy

    if code_point in range(0x80):
        return code_point,
    elif code_point in range(0x0080, 0x0800):
        first = 0b11000000 | (yy & 0b11110111_11111111)  # turn off the 0 bit
        second = x_byte
        return first, second
    elif code_point in range(0x0800, 0xd800) \
            or code_point in range(0xe000, 0x00010000):
        first = 0b11100000 | zz
        second = y_byte
        third = x_byte
        return first, second, third
    elif code_point in range(0x00010000, 0x00110000):
        first = 0b11110000 | (uu >> 2)
        second = 0b10000000 | ((uu & 0b00011) << 4) | zz
        third = y_byte
        fourth = x_byte
        return first, second, third, fourth

    raise UnicodeError('code_point out of range')


@dataclasses.dataclass
class UnicodeBuffer:
    unicode_buffer: typing.List[int] = dataclasses.field(default_factory=list)

    def copy(self):
        return type(self)(
            self.unicode_buffer[:],
        )

    def add_bytes(self, *new_bytes):
        self.unicode_buffer.extend(new_bytes)
        code_points = []

        while self.unicode_buffer:
            n_bytes = get_n_bytes(self.unicode_buffer[0])
            code_point = 0xfffd

            if n_bytes == 0:
                code_points.append(code_point)
                break
            elif n_bytes > len(self.unicode_buffer):
                break

            unicode_bytes = self.unicode_buffer[:n_bytes]
            self.unicode_buffer = self.unicode_buffer[n_bytes:]

            if verify_unicode_bytes(*unicode_bytes):
                code_point = decode_verified(*unicode_bytes)

            code_points.append(code_point)

        return code_points
