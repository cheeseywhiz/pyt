class Store:
    def __init__(self, initial_state):
        self.state = initial_state
        self.subscriptions = []

    def _do_subscriptions(self):
        for subscription in self.subscriptions:
            subscription()

    def dispatch(self, action):
        self.state = self.state.reduce(action)
        self._do_subscriptions()

    def subscribe(self, callback):
        self.subscriptions.append(callback)

        def unsubscribe():
            self.subscriptions.remove(callback)

        return unsubscribe
