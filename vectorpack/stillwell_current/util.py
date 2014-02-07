
class vector(tuple):

    def __add__(self, other):
        if len(self) != len(other):
            return NotImplemented # or raise an error, whatever you prefer
        else:
            return vector(x+y for x,y in zip(self,other))

    def __sub__(self, other):
        if len(self) != len(other):
            return NotImplemented # or raise an error, whatever you prefer
        else:
            return vector(x-y for x,y in zip(self,other))

    def __eq__(self, other):
        return all(x == y for x, y in zip(self, other))
        
    
    def __le__(self, other):

        for x, y in zip(self, other):
            if x > y:
                return False

        return True


def zero(*args, **kwargs):
    """ This function takes any arguments and always returns 0. """
    return 0


def negate_func(func):
    """ returns a function that returns the negation of f """
    return lambda *args, **kwargs: -func(*args, **kwargs)
