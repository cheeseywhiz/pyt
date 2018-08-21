from chars import *


def escape_command(seq):
    return ESC + seq


def control_sequence(final_byte, *args):
    body = SEP.join(map(str, args))
    return escape_command(f'{CSI}{body}{final_byte}')


def cursor_character_absolute(nth_col=None):
    if nth_col is None:
        nth_col = 0

    return control_sequence(CHA, nth_col + 1)


def cursor_forward_tabulation(n_tabs=None):
    if n_tabs is None:
        n_tabs = 1

    return control_sequence(CHT, n_tabs)
