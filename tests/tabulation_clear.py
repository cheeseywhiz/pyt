import pyt.config
from tests import (
    join, tabuation_clear, cursor_character_absolute, character_tabulation_set,
)
from chars import HT, LF

n_tabs = pyt.config.width // pyt.config.tab_width + 1


def set_tab_col(nth_col):
    return join(
        cursor_character_absolute(nth_col),
        character_tabulation_set(),
    )


def reset_tabs():
    return join(*(
        set_tab_col(i * pyt.config.tab_width)
        for i in range(n_tabs)
    ))


def test_tabs():
    return join(
        cursor_character_absolute(),
        ('a' + HT) * (n_tabs + 1),
        LF)


def clear_col(nth_col):
    return join(
        cursor_character_absolute(nth_col),
        tabuation_clear(),
    )


def clear_all():
    return join(
        tabuation_clear(3),
        test_tabs(),
    )


def clear_col_case(nth_col):
    return join(
        clear_col(nth_col),
        test_tabs(),
    )


def main():
    print(test_tabs())
    print(clear_col_case(pyt.config.tab_width * 4))
    print(clear_col_case(pyt.config.width - 1))
    print(clear_all())
    print(reset_tabs())
    print(test_tabs())


if __name__ == '__main__':
    main()
