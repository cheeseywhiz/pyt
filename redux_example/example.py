import pprint
import dataclasses
import redux
from State import State
import actions
import my_selectors

store = redux.Store(State())


def print_state():
    pprint.pprint(dataclasses.asdict(store.state))
    print()


def do_actions(actions_list):
    for action in actions_list:
        print(action)
        store.dispatch(action)

    print()


def main():
    print_state_unsubscribe = store.subscribe(print_state)
    actions1 = [
        actions.UpdateOperation(actions.OperationNames.SCALE),
        actions.SetMatrix.scale(3),
        redux.stack_actions.Push(),
    ]

    actions2 = [
        actions.UpdateOperation(actions.OperationNames.ROTATION),
        actions.SetMatrix.rotation(90),
        redux.stack_actions.Push(),
        actions.UpdateOperation(actions.OperationNames.TRANSLATION),
        actions.SetMatrix(ox=3, oy=4),
    ]

    actions3 = [
        redux.stack_actions.Pop(),
        actions.SetMatrix.Reset(),
        redux.stack_actions.Clear(),
    ]

    print_state()
    do_actions(actions1)
    print_state_unsubscribe()
    do_actions(actions2)
    print_state()

    for frame in my_selectors.globals_(store.state):
        print(frame)

    print()
    print_state_unsubscribe = store.subscribe(print_state)
    do_actions(actions3)


if __name__ == '__main__':
    main()
