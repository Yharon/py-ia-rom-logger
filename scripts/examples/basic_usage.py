from dataclasses import dataclass
from logging import critical, debug, error, exception, info, warning
from typing import Any, Literal

from py_clean_cli import CommandArgsModel, command

from py_ia_rom_logger import LoggingManager


@command(name="basic", help_text="Basic usage of the library")
@dataclass
class BasicUsageCommand(CommandArgsModel):
    """Command to exemplify the basic usage of the library."""

    def exec(self) -> None:
        """
        Implementation of the basic command
        """
        level: Literal['DEBUG', 'INFO'] = "DEBUG" if self.verbose else "INFO"
        LoggingManager().setup_logging(level=level)

        basic_usage_of_the_library()
        if self.verbose:
            uncaught_error()


class CustomModel:

    def __init__(self, name: str, value: int = 10):
        self.name = name
        self.value = value

    def __str__(self):
        return f"CustomModel(name={self.name}, value={self.value})"

    def __repr__(self):
        return self.__str__()

    def to_dict(self) -> dict[str, Any]:
        return {"name": self.name, "value": self.value}



def function_level_1():
    function_level_2()


def function_level_2():
    function_level_3()


def function_level_3():
    result = str(10 / 0)
    return result


def basic_usage_of_the_library():
    """Basic usage of the library."""

    models = [
        CustomModel("Model 1"),
        CustomModel("Model 2"),
        CustomModel("Model 3"),
    ]

    dict_ = {
        "models": models,
        "description": "Example of using the library with custom models",
    }
    print("=== Example 1 Basic Usage of the Library ===")
    print("Should show logs with colors and custom formatting\n")
    info(
        "Process started successfully! 🚀✨ %s%s%s",
        CustomModel("Model 1"),
        CustomModel("Model 2").to_dict(),
        "🥳🥳",
    )
    info("Process started successfully! 🚀✨ %s", CustomModel("Model 1"))
    debug("This is a debug log (DEBUG) %s", dict_)
    warning("This is a warning log (WARNING)")
    error("This is an error log (ERROR)")
    critical("This is a critical log (CRITICAL)")

    try:
        # Simulating an exception
        function_level_1()
    except ZeroDivisionError:
        # raise CustomException("Error of division by zero in the function function_level_3")
        exception(
            "This is an exception log (EXCEPTION) %s", CustomModel("Model 3").to_dict()
        )


def uncaught_error():
    """
    Function that generates an uncaught error to demonstrate the exception log
    """
    # Simula erro de automação
    result = 10 / 0
    return result
