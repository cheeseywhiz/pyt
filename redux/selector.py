__all__ = 'selector',


def selector(*input_selectors):
    def decorator(func):
        def wrapper(state):
            args = (
                input_selector(state)
                for input_selector in input_selectors
            )
            return func(*args)

        return wrapper

    return decorator
