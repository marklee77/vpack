def zero(*args, **kwargs):
    """ This function takes any arguments and always returns 0. """
    return 0


def negate_func(func):
    """ returns a function that returns the negation of f """
    return lambda *args, **kwargs: -func(*args, **kwargs)
