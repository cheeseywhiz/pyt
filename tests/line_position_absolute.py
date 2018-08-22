import pyt.config
from tests import line_position_absolute, reset_to_initial_state, join
from chars import CR


def test_case():
    return join(
        reset_to_initial_state(),
        line_position_absolute(),
        CR, 'hello world',
        line_position_absolute(pyt.config.height // 2),
        CR, 'middle of screen',
        line_position_absolute(pyt.config.height),
        CR, 'goodbye world',
    )


def main():
    print(test_case())


if __name__ == '__main__':
    main()
