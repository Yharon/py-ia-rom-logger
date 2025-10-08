from dataclasses import dataclass, field
from pathlib import Path

from py_ia_rom_logger.helpers.system_info_helper import SystemInfoHelper
from py_ia_rom_logger.models import FileLogModel

from py_ia_rom_logger.config import SETTINGS


@dataclass
class FileManagerService:
    """
    Classe responsável por gerenciar arquivos e diretórios.
    """

    SYS_INFO: SystemInfoHelper = field(init=False, default_factory=SystemInfoHelper)
    FILE_LOG: FileLogModel = field(init=False, default_factory=FileLogModel)

    BACKUP_LOG_DIR: Path = field(init=False)
    FORMAT_LOG_DIR: str = field(init=False, default="%Y-%m/%d")

    def __post_init__(self):
        self._setup_log_dirs()

    def cleanup_old_files(self) -> None:
        """
        Limpa arquivos antigos no diretório de logs de depuração.
        """

        if not self.BACKUP_LOG_DIR.exists():
            return

        # Lista arquivos ordenados por data de modificação
        files = sorted(
            self.BACKUP_LOG_DIR.glob("*.log"), key=lambda f: f.stat().st_mtime
        )

        # Remove arquivos excedentes
        if len(files) >= SETTINGS.MAX_FILES:
            files_to_remove = len(files) - SETTINGS.MAX_FILES + 1
            self._delete_files(files, files_to_remove)

    def _delete_files(self, files: list[Path], qtd: int) -> None:
        """
        Exclui os primeiros arquivos de uma lista de caminhos de arquivos.
        """
        for file_path in files[:qtd]:
            try:
                file_path.unlink()
            except OSError:
                pass

    def _setup_log_dirs(self) -> None:
        """Configura diretórios de log."""

        # Diretório para logs diários
        date_format = self.SYS_INFO.timestamp.strftime(self.FORMAT_LOG_DIR)

        self.BACKUP_LOG_DIR = SETTINGS.LOG_DIR / date_format
        self.BACKUP_LOG_DIR.mkdir(parents=True, exist_ok=True)
