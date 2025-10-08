"""Decorators for enhancing class and function functionality."""


def singleton(cls):
    """Decorator that implements the singleton pattern for a class.

    Ensures only one instance of the decorated class exists throughout
    the application lifecycle. Useful for managing shared resources
    like configuration or database connections.

    Args:
        cls: The class to be converted to a singleton.

    Returns:
        function: Wrapper function that returns the singleton instance.

    Examples:
        >>> @singleton
        ... class Config:
        ...     def __init__(self, value):
        ...         self.value = value
        ...
        >>> config1 = Config(10)
        >>> config2 = Config(20)
        >>> config1 is config2  # Same instance
        True
    """
    # 🏗️ Architecture: Cache instances to ensure singleton pattern
    instances = {}

    def getinstance(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return getinstance
