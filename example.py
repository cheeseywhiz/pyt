import pprint
import dataclasses
from Store import Store
from State import State
import actions

store = Store(State())


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
        actions.Stack.Push(),
    ]

    actions2 = [
        actions.UpdateOperation(actions.OperationNames.ROTATION),
        actions.SetMatrix.rotation(90),
        actions.Stack.Push(),
    ]

    actions3 = [
        actions.Stack.Pop(),
        actions.SetMatrix.Reset(),
        actions.Stack.Clear(),
    ]

    print_state()
    do_actions(actions1)
    print_state_unsubscribe()
    do_actions(actions2)
    print_state()
    print()
    print_state_unsubscribe = store.subscribe(print_state)
    do_actions(actions3)


if __name__ == '__main__':
    main()
