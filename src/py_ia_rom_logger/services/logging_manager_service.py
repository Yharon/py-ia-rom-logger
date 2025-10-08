"""Gerenciador principal do sistema de logging.

Este módulo contém a classe principal que coordena todos os handlers
e configurações do sistema de logging, implementando o padrão Singleton.

Examples
--------
>>> from rich_logger.helpers.logging_manager import LoggingManager
>>> manager = LoggingManager()
>>> manager.setup_logging()
"""

import threading
import logging
import sys
from dataclasses import dataclass, field
from typing import Optional

from py_ia_rom_logger.config.decorators import singleton
from py_ia_rom_logger.handlers import (
    ConsoleHandler,
    AvailableFormatters,
    JsonCustomFileHandler,
    AvailableFileFormatters,
)


def _install_sys_excepthook(logger_: logging.Logger) -> None:
    """Registra exceções não tratadas no logger."""

    def _hook(exc_type, exc_value, exc_tb):
        msg = "Unhandled exception"
        # Registra interrupções de teclado
        if issubclass(exc_type, KeyboardInterrupt):
            msg = "Keyboard interrupt exception"
        logger_.critical(msg, exc_info=(exc_type, exc_value, exc_tb))
    sys.excepthook = _hook


def _install_threading_excepthook(logger_: logging.Logger) -> None:
    """Para Python ≥3.8: captura exceções em threads."""

    if hasattr(threading, "excepthook"):
        def _thread_hook(args: threading.ExceptHookArgs):  # type: ignore[attr-defined]
            name_ = args.thread.name if args.thread else "MainThread"
            msg = "Unhandled exception"
            if issubclass(args.exc_type, KeyboardInterrupt):
                msg = "Keyboard interrupt exception"
            logger_.critical(
                f"{msg} in thread {name_}",
                exc_info=(args.exc_type, args.exc_value, args.exc_traceback),  # type: ignore[attr-defined]
            )
        threading.excepthook = _thread_hook


@singleton
@dataclass
class LoggingManager:
    """Gerenciador principal do sistema de logging.

    Esta classe implementa o padrão Singleton para garantir que apenas uma
    instância do gerenciador seja criada durante toda a execução do programa.

    Responsabilidades:
    - Configurar handlers de console, arquivo e HTML
    - Gerenciar diretórios de log
    - Limpar arquivos antigos
    - Coordenar formatadores

    Examples
    --------
    >>> manager = LoggingManager()
    >>> manager.setup_logging()
    >>> # Usar logging normalmente
    >>> import logging
    >>> logging.info("Sistema iniciado")
    """

    RICH_HANDLER: ConsoleHandler = field(init=False, default_factory=ConsoleHandler)
    FILE_HANDLER: JsonCustomFileHandler = field(
        init=False, default_factory=JsonCustomFileHandler
    )
    LOGGER: logging.Logger = field(init=False, default_factory=logging.getLogger)

    def setup_logging(
        self,
        *,
        console_formatter: AvailableFormatters = AvailableFormatters.RICH,
        file_formatter: AvailableFileFormatters = AvailableFileFormatters.JSON,
        level: str = "DEBUG",
    ) -> None:
        """
        Configura o sistema de logging completo.

        Cria e configura todos os handlers necessários:
        - Console handler com Rich formatting
        - Arquivo de log principal (app.log)
        - Arquivo MD principal (app.md) com nível DEBUG
        - Arquivo MD de histórico (timestamped)

        Examples
        --------
        >>> manager = LoggingManager()
        >>> manager.setup_logging("meu_app.log")
        """
        # Verifica se já foi configurado
        if self.LOGGER.hasHandlers():
            return

        # Cria handlers
        console_handler = self.RICH_HANDLER.create_rich_handler(console_formatter)
        file_handler = self.FILE_HANDLER.create_file_handler(file_formatter)

        # Adiciona handlers ao logger
        self.LOGGER.addHandler(console_handler)
        self.LOGGER.addHandler(file_handler)

        # Define nível global
        self.LOGGER.setLevel(level)

        _install_sys_excepthook(self.LOGGER)
        _install_threading_excepthook(self.LOGGER)

    def get_logger(self, name: Optional[str] = None) -> logging.Logger:
        """Retorna logger configurado.

        Parameters
        ----------
        name : str, optional
            Nome do logger, by default None

        Returns
        -------
        logging.Logger
            Logger configurado e pronto para uso
        """
        if name:
            return logging.getLogger(name)
        return self.LOGGER
