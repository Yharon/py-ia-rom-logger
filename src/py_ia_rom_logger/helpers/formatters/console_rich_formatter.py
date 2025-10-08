"""Formatter personalizado para logs com formatação Rich.

Este módulo contém a implementação do formatter que aplica formatação
Rica às mensagens de log, incluindo cores, estilos e estruturação
visual das informações.

Examples
--------
>>> from rpa_logger.formatters.rich_formatter import RichFormatter
>>> formatter = RichFormatter()
>>> handler.setFormatter(formatter)
"""

import logging
from types import TracebackType

from rich.console import ConsoleRenderable, Group
from rich.markup import escape
from rich.text import Text
from rich.panel import Panel
from rich.json import JSON

from py_ia_rom_logger.models import ConsoleLogModel
from .tracebacks.console_rich_traceback_formatter import TracebackRichFormatter

from . import AbstractConsoleCustomFormatter


class RichFormatter(AbstractConsoleCustomFormatter):
    """
    Formatter personalizado com formatação Rich para logs.

    Este formatter aplica formatação Rich às mensagens de log,
    incluindo cores específicas para cada nível, formatação de
    timestamp e estruturação visual das informações.

    Examples
    --------
    >>> formatter = RichFormatter(console)
    >>> handler.setFormatter(formatter)
    """

    def __init__(self):
        super().__init__()

        self._console_model = ConsoleLogModel()
        self._traceback = TracebackRichFormatter()

    def format_level(self, record: logging.LogRecord) -> str:
        """Retorna o código de nível de 4 letras com cor.

        Parameters
        ----------
        record : logging.LogRecord
            Registro de log

        Returns
        -------
        str
            Código de nível de 4 letras com cor Rich
        """
        level_name = record.levelname
        short_name = self._console_model.level_map.get(level_name, level_name[:4])
        color = self._console_model.rich_theme.styles.get(
            f"logging.level.{level_name}", ""
        )
        return Text(short_name, style=color).markup

    def format_message(self, record: logging.LogRecord) -> str:
        """
        Formata a mensagem do log.

        Returns
        -------
        str
            Mensagem formatada com Rich markup
        """
        message = escape(record.getMessage())
        color = self._console_model.rich_theme.styles.get(
            f"logging.message.{record.levelname}", ""
        )
        return Text(message, style=color).markup

    def format_arguments(self, record: logging.LogRecord) -> ConsoleRenderable:
        """
        Formata os argumentos do log.

        Parameters
        ----------
        message : str
            Mensagem base do log
        args : Any
            Argumentos passados ao log (pode ser tupla, dict, etc.)

        Returns
        -------
        tuple[str, Any]
            Mensagem e argumentos formatados com Rich markup
        """
        renderables: list[ConsoleRenderable] = []
        message = escape(record.msg)
        color = self._console_model.rich_theme.styles.get(
            f"logging.message.{record.levelname}", ""
        )

        msg_formatted = self._console_model.remove_placeholders(message)
        renderables.append(Text(msg_formatted, style=color))

        payload = (
            self._console_model.jsonable(record.args[0])
            if isinstance(record.args, tuple) and len(record.args) == 1
            else self._console_model.jsonable(record.args)
        )

        panel = Panel.fit(
            JSON.from_data(payload),
            title="Arguments",
            title_align="left",
            border_style=color,
        )
        renderables.append(panel)

        return Group(*renderables)

    def format_exception(
        self,
        ei: (
            tuple[type[BaseException], BaseException, TracebackType | None]
            | tuple[None, None, None]
        ),
    ) -> tuple[str, str]:
        """
        Formata a exceção do log, se houver.

        Parameters
        ----------
        record : logging.LogRecord
            Registro de log

        Returns
        -------
        str
            Traceback formatado com Rich markup, ou string vazia se não houver exceção
        """
        if not ei or ei == (None, None, None):
            return "", ""

        exc_type, exc_value, exc_traceback = ei
        if not exc_type or not exc_value or not exc_traceback:
            return "", ""

        return (
            self._traceback.create_rich_traceback(exc_type, exc_value, exc_traceback),
            self._traceback.exc_title
        )
