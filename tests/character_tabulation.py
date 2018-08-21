import pyt.config
from tests import cursor_character_absolute
from chars import HT


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
