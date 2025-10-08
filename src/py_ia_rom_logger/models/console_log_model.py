from functools import cached_property
from dataclasses import dataclass, field

from rich.console import Console

from . import LogModel, CustomThemes


@dataclass
class ConsoleLogModel(LogModel):
    """
    Modelo de log para saída no console
    """
    THEMES: CustomThemes = field(init=False, default_factory=CustomThemes)

    def __post_init__(self):

        self.DEFAULT_THEME = self.THEMES.DEFAULT
        self.RICH_THEME = self.THEMES.RICH

    @cached_property
    def rich_theme(self):
        return self.RICH_THEME

    def create_standard_console(self) -> Console:
        """
        Cria um console Rich com o tema padrão.
        """
        return Console(theme=self.DEFAULT_THEME)

    def create_rich_console(self, **kwargs) -> Console:
        """
        Cria um console Rich com o tema Rich.
        """

        kwargs.setdefault("theme", self.RICH_THEME)

        kwargs.get("tracebacks_suppress", ["*"])
        kwargs.setdefault("log_path", False)

        return Console(**kwargs)
