def doc(docstring):
    """Декоратор для установки docstring."""

    def decorator(func):
        func.__doc__ = docstring
        return func

    return decorator
