import logging
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from types import TracebackType
from typing import Optional

from rich.console import ConsoleRenderable


@dataclass
class AbstractConsoleCustomFormatter(logging.Formatter, ABC):
    """
    Modelo de formatação personalizada para logs Rich.
    Este modelo define a estrutura básica para formatação de logs,
    incluindo temas e formatação de mensagens.

    Attributes
    ----------
    fmt : str, optional
        String de formato para logs
    datefmt : str, optional
        String de formato para datas
    """

    fmt: Optional[str] = field(default=None)
    datefmt: Optional[str] = field(default=None)

    def __post_init__(self):
        """Inicializa o Formatter pai após criação do dataclass."""
        super().__init__(fmt=self.fmt, datefmt=self.datefmt, style="{")

    @abstractmethod
    def format_level(self, record: logging.LogRecord) -> str:
        """
        Formata o nível de log.
        """

    @abstractmethod
    def format_message(self, record: logging.LogRecord) -> str:
        """
        Formata a mensagem de log.
        """

    @abstractmethod
    def format_exception(
        self,
        ei: (
            tuple[type[BaseException], BaseException, TracebackType | None]
            | tuple[None, None, None]
        ),
    ) -> tuple[str, str]:
        """
        Formata a exceção do log.
        """

    @abstractmethod
    def format_arguments(self, record: logging.LogRecord) -> ConsoleRenderable:
        """
        Formata os argumentos do log.
        """
