import pyt
from tests import join, cursor_forward_tabulation, cursor_character_absolute


def test_case(n_cols, n_tabs):
    return join(
        cursor_character_absolute(n_cols),
        'a',
        cursor_forward_tabulation(n_tabs),
        'b',
    )


def main():
    n_tabs = pyt.config.width // pyt.config.tab_width

    for i in range(pyt.config.width - 8, pyt.config.width):
        for j in range(n_tabs + 10):
            print(test_case(i, j))


if __name__ == '__main__':
    main()
