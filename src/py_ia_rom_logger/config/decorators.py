"""
A collection of decorators for various purposes.
This module provides decorators that can be used to enhance the functionality of classes and functions.
"""

def singleton(cls):
    """
    A decorator to make a class a singleton
    pattern, ensuring that only one instance of the class is created.
    This is useful for classes that manage shared resources or configurations.

    Example
    -------
    >>> @singleton
    >>> class MySingletonClass:
    >>>     def __init__(self, value):
    >>>         self.value = value
    """
    instances = {}

    def getinstance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return getinstance
