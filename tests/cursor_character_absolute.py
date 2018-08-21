import pyt.config
from tests import join, cursor_character_absolute


def test_case(nth_col):
    return join(
        cursor_character_absolute(nth_col),
        'a',
    )


def main():
    for i in range(pyt.config.width + 10):
        print(test_case(i))


if __name__ == '__main__':
    main()
