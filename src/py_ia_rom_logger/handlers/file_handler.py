import logging
from enum import Enum

from py_ia_rom_logger.helpers.formatters import SafeJsonFormatter
from py_ia_rom_logger.services import FileManagerService


class AvailableFileFormatters(Enum):
    """
    Formatação disponível para arquivos de log
    """

    JSON = SafeJsonFormatter(
        fmt=(
            "%(asctime)s %(levelname)s %(name)s %(message)s "
            "%(filename)s %(funcName)s %(lineno)d "
            "%(threadName)s %(process)d"
        ),
        datefmt="%Y-%m-%dT%H:%M:%S%z",
        json_ensure_ascii=False,
    )


class JsonCustomFileHandler(logging.FileHandler):

    _file_manager = FileManagerService()

    def __init__(self, **kwargs):

        kwargs.setdefault("filename", self._create_log_path_name())
        kwargs.setdefault("mode", "w")
        kwargs.setdefault("encoding", "utf-8")

        super().__init__(**kwargs)

    @classmethod
    def create_file_handler(
        cls, formatter: AvailableFileFormatters, **kwargs
    ) -> "JsonCustomFileHandler":
        """
        Cria uma instância do FileHandler com configurações personalizadas.
        """
        cls._file_manager.cleanup_old_files()

        cls._formatter = formatter.value
        file_handler = cls(**kwargs)

        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(cls._formatter)

        return file_handler

    def _create_log_path_name(self) -> str:
        """
        Cria o caminho completo do arquivo de log.
        """
        filename = self._file_manager.FILE_LOG.create_log_file_name()
        file_path = self._file_manager.BACKUP_LOG_DIR / filename

        return str(file_path)
