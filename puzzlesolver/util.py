class PuzzleValue:
    SOLVABLE = "SOLVABLE"
    UNSOLVABLE = "UNSOLVABLE"
    UNDECIDED = "UNDECIDED"

    @staticmethod
    def contains(key):
        return (key == PuzzleValue.SOLVABLE or 
                key == PuzzleValue.UNSOLVABLE or 
                key == PuzzleValue.UNDECIDED)

class PuzzleException(Exception):
    """An Exception meant to be caught by the server"""
    pass

class ClassPropertyDescriptor(object):
    def __init__(self, fget, fset=None):
        self.fget = fget
        self.fset = fset

    def __get__(self, obj, klass=None):
        if klass is None:
            klass = type(obj)
        return self.fget.__get__(obj, klass)()

    def __set__(self, obj, value):
        if not self.fset:
            raise AttributeError("can't set attribute")
        type_ = type(obj)
        return self.fset.__get__(obj, type_)(value)

    def setter(self, func):
        if not isinstance(func, (classmethod, staticmethod)):
            func = classmethod(func)
        self.fset = func
        return self    

def classproperty(func):
    if not isinstance(func, (classmethod, staticmethod)):
        func = classmethod(func)
    return ClassPropertyDescriptor(func)

import warnings

def depreciated(msg):
    def decorator(func):
        def wrapper(*args, **kwargs):
            warnings.warn(msg, DeprecationWarning)
            return func(*args, **kwargs)
        return wrapper
    return decorator
    
