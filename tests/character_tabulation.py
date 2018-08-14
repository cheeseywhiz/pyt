import pyt.config


HT = chr(0x09)
LF = chr(0x0a)
ESC = chr(0x1b)
SEP = chr(0x3b)
CHA = chr(0x47)
CSI = chr(0x5b)


def escape_command(seq):
    return ESC + seq


def control_sequence(final_byte, *args):
    body = SEP.join(map(str, args))
    return escape_command(f'{CSI}{body}{final_byte}')


def cursor_character_absolute(nth_col=None):
    if nth_col is None:
        nth_col = 0

    return control_sequence(CHA, nth_col + 1)


def test_case(nth_col):
    return ''.join([
        cursor_character_absolute(nth_col),
        'a', HT, 'b',
    ])


def main():
    for i in range(pyt.config.width):
        print(test_case(i))


if __name__ == '__main__':
    main()
