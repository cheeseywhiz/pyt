import pyt.config
from tests import line_position_absolute, reset_to_initial_state, join
from chars import CR, LF


def test_case():
    return join(
        reset_to_initial_state(),
        'hello world', LF,
        'super long text string under hello world',
        line_position_absolute(pyt.config.height // 2),
        CR, 'middle of screen', LF,
        'second middle line',
        line_position_absolute(pyt.config.height),
        CR, 'goodbye world', LF,
        'second line of bottom',
        line_position_absolute(),
        CR, 'overwrite new top line',
    )


def main():
    print(test_case())


if __name__ == '__main__':
    main()
