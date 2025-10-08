import logging
from enum import Enum

from rich.console import ConsoleRenderable
from rich.logging import RichHandler
from rich.panel import Panel
from rich.text import Text

from py_ia_rom_logger.config import SETTINGS
from py_ia_rom_logger.helpers.formatters import (
    AbstractConsoleCustomFormatter,
    RichFormatter,
)
from py_ia_rom_logger.models import ConsoleLogModel


class AvailableFormatters(Enum):
    """
    Formatação disponível para logs Rich.
    Esta classe contém os formatadores disponíveis para logs Rich,
    incluindo o RichFormatter padrão.
    Attributes
    ----------
    rich: RichFormatter
        Formatação Rich padrão para logs.
    """

    RICH = RichFormatter()


class ConsoleHandler(RichHandler):
    """
    Handler personalizado Rich com códigos de nível de 4 letras.

    Este handler estende o RichHandler padrão para fornecer:
    - Códigos de nível de 4 letras (DEBG, INFO, WARN, ERRO, CRIT)
    - Cores personalizadas para cada nível
    - Formatação consistente de mensagens
    - Ícones e símbolos visuais

    Parameters
    ----------
    console : Console, optional
        Instância do console Rich a ser usada
    **kwargs
        Argumentos adicionais passados para RichHandler

    Examples
    --------
    >>> console = Console()
    >>> handler = ConsoleHandler(console=console)
    >>>
    >>> handler.setLevel(logging.DEBUG)
    >>> logger.addHandler(handler)
    """

    _formatter: AbstractConsoleCustomFormatter
    _console_log = ConsoleLogModel()

    def __init__(self, **kwargs):
        """
        Inicializa o ConsoleHandler com um console Rich.

        Parameters
        ----------
        console : ConsoleRenderable, optional
            Instância do console Rich a ser usada
        **kwargs
            Argumentos adicionais passados para RichHandler
        """

        kwargs.setdefault("show_path", False)
        kwargs.setdefault("enable_link_path", False)
        kwargs.setdefault("log_time_format", f"[{SETTINGS.TIMESTAMP_FORMAT}]")
        kwargs.setdefault("rich_tracebacks", False)
        kwargs.setdefault("tracebacks_max_frames", SETTINGS.TRACEBACKS_MAX_FRAMES)
        kwargs.setdefault("tracebacks_extra_lines", SETTINGS.TRACEBACKS_MAX_FRAMES)
        kwargs.setdefault("console", self._console_log.create_rich_console())

        super().__init__(**kwargs)

    @classmethod
    def create_rich_handler(
        cls, formatter: AvailableFormatters, **kwargs
    ) -> "ConsoleHandler":
        """
        Cria uma instância do ConsoleHandler com configurações personalizadas.

        Parameters
        ----------
        console : Console, optional
            Instância do console Rich a ser usada
        **kwargs
            Argumentos adicionais passados para RichHandler
        """

        cls._formatter = formatter.value
        rich_handler = cls(**kwargs)

        rich_handler.setLevel(logging.DEBUG)
        rich_handler.setFormatter(cls._formatter)

        return rich_handler

    def get_level_text(self, record: logging.LogRecord) -> Text:
        """
        Retorna o texto do nível de log formatado.
        Essa função é especificamente usada para obter o texto do nível de log
        formatado com cor Rich. Nenhuma outra função formata o nível de log.

        Parameters
        ----------
        record : logging.LogRecord
            Registro de log
        Returns
        -------
        Text
            Texto do nível de log formatado com cor Rich
        """
        return Text.from_markup(self._formatter.format_level(record))

    def render_message(
        self, record: logging.LogRecord, message: str
    ) -> ConsoleRenderable:
        """
        Renderiza a mensagem do log com formatação Rich.
        Essa função é usada para renderizar a mensagem do log
        com formatação Rich, aplicando estilos e cores apropriados.
        Ela especificamente formata a mensagem do log, não mexendo
        com o nível de log ou outros aspectos do registro.

        Parameters
        ----------
        record : logging.LogRecord
            Registro de log
        message : str
            Mensagem a ser renderizada

        Returns
        -------
        ConsoleRenderable
            Mensagem renderizada com formatação Rich
        """
        if record.args:
            return self._formatter.format_arguments(record)
        msg_formatted = self._formatter.format_message(record)
        return Text.from_markup(msg_formatted)

    def emit(self, record: logging.LogRecord) -> None:
        """
        Emite log com visual aprimorado.
        Este método é chamado para emitir um registro de log.
        Ele formata a mensagem e o nível de log, e exibe o traceback se houver uma exceção associada.
        Essa função é usada apenas para emitir as exceções nos logs. Ela sobrescreve qualquer outra função
        que possa emitir logs, garantindo que a formatação da exception seja aplicada corretamente.

        Parameters
        ----------
        record : logging.LogRecord
            Registro de log a ser emitido

        Raises
        ------
        Exception
            Se ocorrer um erro ao emitir o registro de log
        """
        try:
            if record.exc_info and record.levelno >= logging.ERROR:
                self._format_print_exc(record.getMessage(), record.exc_info)
            else:
                super().emit(record)
        except Exception:
            self.handleError(record)

    def _format_print_exc(self, text_log: str, exc_info) -> None:

        log_exc = self._formatter.format_exception(exc_info)
        text_exc = log_exc[0]
        title_exc = log_exc[1]

        self.console.print()
        self.console.print(text_log, style="bold white on red", justify="center")

        panel = Panel(
            text_exc,
            title=title_exc,
            title_align="left",
            border_style="red",
        )
        self.console.print(panel)
        self.console.print()
