"""Tests for FileManagerService."""

from pathlib import Path

import pytest

from py_ia_rom_logger.services.file_manager_service import FileManagerService


class TestFileManagerService:
    """Test suite for FileManagerService."""

    def test_initialization_creates_backup_dir(self, tmp_path, monkeypatch):
        """Test FileManagerService creates backup log directory."""
        log_dir = tmp_path / "logs"
        log_dir.mkdir()

        monkeypatch.setattr(
            "py_ia_rom_logger.services.file_manager_service.SETTINGS.LOG_DIR",
            log_dir,
        )

        manager = FileManagerService()

        # Should create dated subdirectory
        assert manager.BACKUP_LOG_DIR.exists()
        assert manager.BACKUP_LOG_DIR.is_dir()

    def test_backup_dir_structure(self, tmp_path, monkeypatch):
        """Test backup directory follows YYYY-MM/DD format."""
        log_dir = tmp_path / "logs"
        log_dir.mkdir()

        monkeypatch.setattr(
            "py_ia_rom_logger.services.file_manager_service.SETTINGS.LOG_DIR",
            log_dir,
        )

        manager = FileManagerService()

        # Path should contain date structure
        path_parts = manager.BACKUP_LOG_DIR.parts
        # Should have format like: .../logs/YYYY-MM/DD
        assert len(path_parts) >= 3

    def test_cleanup_old_files_removes_excess(self, tmp_path, monkeypatch):
        """Test cleanup_old_files removes oldest files."""
        log_dir = tmp_path / "logs" / "2024-01" / "15"
        log_dir.mkdir(parents=True)

        monkeypatch.setattr(
            "py_ia_rom_logger.services.file_manager_service.SETTINGS.LOG_DIR",
            tmp_path / "logs",
        )
        monkeypatch.setattr(
            "py_ia_rom_logger.services.file_manager_service.SETTINGS.MAX_FILES",
            5,
        )

        # Create 10 old log files
        for i in range(10):
            (log_dir / f"old_{i}.log").touch()

        manager = FileManagerService()
        manager.BACKUP_LOG_DIR = log_dir

        manager.cleanup_old_files()

        # Should keep only MAX_FILES (5)
        remaining_files = list(log_dir.glob("*.log"))
        assert len(remaining_files) <= 5

    def test_cleanup_old_files_keeps_newest(self, tmp_path, monkeypatch):
        """Test cleanup keeps newest files."""
        log_dir = tmp_path / "logs" / "2024-01" / "15"
        log_dir.mkdir(parents=True)

        monkeypatch.setattr(
            "py_ia_rom_logger.services.file_manager_service.SETTINGS.LOG_DIR",
            tmp_path / "logs",
        )
        monkeypatch.setattr(
            "py_ia_rom_logger.services.file_manager_service.SETTINGS.MAX_FILES",
            3,
        )

        # Create files with different timestamps
        import time

        files = []
        for i in range(5):
            file_path = log_dir / f"log_{i}.log"
            file_path.touch()
            files.append(file_path)
            time.sleep(0.02)  # Ensure different timestamps

        manager = FileManagerService()
        manager.BACKUP_LOG_DIR = log_dir

        manager.cleanup_old_files()

        # Should have removed old files
        remaining_files = list(log_dir.glob("*.log"))

        # Should have at most MAX_FILES
        assert len(remaining_files) <= 3

    def test_cleanup_does_nothing_if_dir_missing(self, tmp_path, monkeypatch):
        """Test cleanup_old_files handles missing directory gracefully."""
        monkeypatch.setattr(
            "py_ia_rom_logger.services.file_manager_service.SETTINGS.LOG_DIR",
            tmp_path / "logs",
        )

        manager = FileManagerService()
        manager.BACKUP_LOG_DIR = tmp_path / "nonexistent"

        # Should not raise
        manager.cleanup_old_files()

    def test_cleanup_does_nothing_under_limit(self, tmp_path, monkeypatch):
        """Test cleanup doesn't remove files under MAX_FILES limit."""
        log_dir = tmp_path / "logs" / "2024-01" / "15"
        log_dir.mkdir(parents=True)

        monkeypatch.setattr(
            "py_ia_rom_logger.services.file_manager_service.SETTINGS.LOG_DIR",
            tmp_path / "logs",
        )
        monkeypatch.setattr(
            "py_ia_rom_logger.services.file_manager_service.SETTINGS.MAX_FILES",
            10,
        )

        # Create only 3 files (under limit)
        for i in range(3):
            (log_dir / f"log_{i}.log").touch()

        manager = FileManagerService()
        manager.BACKUP_LOG_DIR = log_dir

        manager.cleanup_old_files()

        # All files should remain
        remaining_files = list(log_dir.glob("*.log"))
        assert len(remaining_files) == 3
