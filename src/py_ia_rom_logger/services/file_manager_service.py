from dataclasses import dataclass, field
from pathlib import Path

from py_ia_rom_logger.helpers.system_info_helper import SystemInfoHelper
from py_ia_rom_logger.models import FileLogModel

from py_ia_rom_logger.config import SETTINGS


@dataclass
class FileManagerService:
    """File and directory manager for log files.

    Handles log directory setup, file rotation, and cleanup.

    Attributes:
        SYS_INFO: System information helper.
        FILE_LOG: File log model for naming.
        BACKUP_LOG_DIR: Directory for backup logs.
        FORMAT_LOG_DIR: Date format for log directory structure.
    """

    SYS_INFO: SystemInfoHelper = field(init=False, default_factory=SystemInfoHelper)
    FILE_LOG: FileLogModel = field(init=False, default_factory=FileLogModel)

    BACKUP_LOG_DIR: Path = field(init=False)
    FORMAT_LOG_DIR: str = field(init=False, default="%Y-%m/%d")

    def __post_init__(self):
        self._setup_log_dirs()

    def cleanup_old_files(self) -> None:
        """Clean up old log files exceeding retention limit.

        Removes oldest files when count exceeds MAX_FILES setting.
        """
        if not self.BACKUP_LOG_DIR.exists():
            return

        # List files sorted by modification time
        files = sorted(
            self.BACKUP_LOG_DIR.glob("*.log"), key=lambda f: f.stat().st_mtime
        )

        # Remove excess files
        if len(files) >= SETTINGS.MAX_FILES:
            files_to_remove = len(files) - SETTINGS.MAX_FILES + 1
            self._delete_files(files, files_to_remove)

    def _delete_files(self, files: list[Path], qtd: int) -> None:
        """Delete first N files from list.

        Args:
            files: List of file paths to delete from.
            qtd: Quantity of files to delete.
        """
        for file_path in files[:qtd]:
            try:
                file_path.unlink()
            except OSError:
                pass

    def _setup_log_dirs(self) -> None:
        """Set up log directory structure.

        Creates dated subdirectories for log organization.
        """
        # Directory for daily logs
        date_format = self.SYS_INFO.timestamp.strftime(self.FORMAT_LOG_DIR)

        self.BACKUP_LOG_DIR = SETTINGS.LOG_DIR / date_format
        self.BACKUP_LOG_DIR.mkdir(parents=True, exist_ok=True)
