import functools
import multiprocessing

__all__ = 'make_process'


def get_decorator(process_kwargs):
    def decorator(target):
        @functools.wraps(target)
        def wrapped(*args, **kwargs):
            process = multiprocessing.Process(
                target=target, args=args, kwargs=kwargs, **process_kwargs)
            process.start()
            return process

        return wrapped

    return decorator


def make_process(target=None, **process_kwargs):
    if target is None:
        # @make_process(daemon=True)
        # def target():
        #     pass
        return get_decorator(process_kwargs)
    else:
        # @make_process
        # def target():
        #     pass
        # or
        # target = make_process(target, daemon=True)
        return get_decorator(process_kwargs)(target)
