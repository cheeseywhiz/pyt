from chars import *


def join(*lines):
    return ''.join(lines)


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


def tabuation_clear(selection=None):
    if selection is None:
        selection = 0

    return control_sequence(TBC, selection)


def character_tabulation_set():
    return escape_command(HTS)


def line_position_absolute(nth_line=None):
    if nth_line is None:
        nth_line = 1

    return control_sequence(VPA, nth_line)


def reset_to_initial_state():
    return escape_command(RIS)
