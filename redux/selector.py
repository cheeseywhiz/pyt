__all__ = 'selector',


def selector(*input_selectors):
    def decorator(func):
        cache_state = None
        cache_result = None

        def wrapper(state):
            nonlocal cache_state, cache_result

            if state is cache_state:
                return cache_result
            else:
                cache_state = state

            args = (
                input_selector(state)
                for input_selector in input_selectors
            )
            cache_result = func(*args)
            return cache_result

        return wrapper

    return decorator
