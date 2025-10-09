from functools import cached_property
from dataclasses import dataclass, field

from rich.console import Console

from . import LogModel, CustomThemes


@dataclass
class ConsoleLogModel(LogModel):
    """Log model for console output with Rich theming.

    Attributes:
        THEMES: Collection of available console themes.
    """

    THEMES: CustomThemes = field(init=False, default_factory=CustomThemes)

    def __post_init__(self):
        self.DEFAULT_THEME = self.THEMES.DEFAULT
        self.RICH_THEME = self.THEMES.RICH

    @cached_property
    def rich_theme(self):
        """Get the Rich theme for console output.

        Returns:
            Theme: Configured Rich theme.
        """
        return self.RICH_THEME

    def create_standard_console(self) -> Console:
        """Create a Rich console with default theme.

        Returns:
            Console: Console instance with default theme.
        """
        return Console(theme=self.DEFAULT_THEME)

    def create_rich_console(self, **kwargs) -> Console:
        """Create a Rich console with Rich theme and custom settings.

        Args:
            **kwargs: Additional console configuration options.

        Returns:
            Console: Configured Rich console instance.
        """
        kwargs.setdefault("theme", self.RICH_THEME)
        kwargs.get("tracebacks_suppress", ["*"])
        kwargs.setdefault("log_path", False)

        return Console(**kwargs)
