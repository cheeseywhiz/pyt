def decode(byte_sequence):
    first = byte_sequence[0]

    if first in range(0x80):
        return first
    elif first in range(0xc2, 0xe0):
        n_bytes = 2
    elif first in range(0xe0, 0xf0):
        n_bytes = 3
    elif first in range(0xf0, 0xf5):
        n_bytes = 4
    else:
        raise UnicodeError('first byte malformed')

    if len(byte_sequence) != n_bytes:
        raise UnicodeError('wrong number of bytes')

    second = byte_sequence[1]

    if n_bytes == 2:
        if first in range(0xc2, 0xe0) and second in range(0x80, 0xc0):
            xx = second & 0b00111111
            yy = (first & 0b0011111) << 6
            return yy | xx
        else:
            raise UnicodeError('2 byte sequence malformed')

    third = byte_sequence[2]

    if n_bytes == 3:
        if third in range(0x80, 0xc0) and (
                (second in range(0x80, 0xc0) and (first in range(0xe1, 0xed) or
                                                  first in range(0xee, 0xf0)))
                or (second in range(0xa0, 0xc0) and first == 0xe0)
                or (second in range(0x80, 0xa0) and first == 0xed)
        ):
            xx = third & 0b00111111
            yy = (second & 0b00111111) << 6
            zz = (first & 0b00001111) << 12
            return zz | yy | xx
        else:
            raise UnicodeError('3 byte sequence malformed')

    fourth = byte_sequence[3]

    if n_bytes == 4:
        if fourth in range(0x80, 0xc0) and third in range(0x80, 0xc0) and (
                (second in range(0x90, 0xc0) and first == 0xf0)
                or (second in range(0x80, 0xc0) and first in range(0xf1, 0xf4))
                or (second in range(0x80, 0x90) and first == 0xf4)
        ):
            xx = fourth & 0b00111111
            yy = (third & 0b00111111) << 6
            zz = (second & 0b00001111) << 12
            uu = (
                ((first & 0b00000111) << 2) | ((second & 0b00110000) >> 4)
            ) << 16
            return uu | zz | yy | xx
        else:
            raise UnicodeError('4 byte sequence malformed')

    raise UnicodeError('Should never make it here')


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


def map_chain(iterable, *funcs):
    ret = iterable

    for func in funcs:
        ret = map(func, ret)

    return ret


def test_string(string):
    return string == ''.join(map_chain(string, ord, encode, decode, chr))


def test():
    for code_point in range(0x00110000):
        new_code_point = None
        status = None

        try:
            byte_sequence = encode(code_point)
        except UnicodeError:
            status = 'ENCODE'
            byte_sequence = [-1]

        try:
            new_code_point = decode(byte_sequence)
        except UnicodeError:
            if status is None:
                status = 'DECODE'

        if status is None:
            status = 'PASS' if code_point == new_code_point else 'FAIL'

        print('\t'.join(map(str, [
            status, hex(code_point), hex(new_code_point or -1),
        ])))
