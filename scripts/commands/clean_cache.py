from __future__ import annotations

import os
import shutil
from pathlib import Path


def _remove_path(path: Path) -> None:
    if not path.exists():
        return
    if path.is_file() or path.is_symlink():
        try:
            path.unlink()
        except FileNotFoundError:
            pass
        return
    shutil.rmtree(path, ignore_errors=True)


def _iter_pycache_dirs(root: Path) -> list[Path]:
    return [p for p in root.rglob("__pycache__") if p.is_dir()]


def clean_local_artifacts(project_root: Path) -> None:
    artifacts = [
        project_root / "build",
        project_root / "dist",
        project_root / ".pytest_cache",
        project_root / ".mypy_cache",
        project_root / ".ruff_cache",
        project_root / "htmlcov",
        project_root / ".coverage",
        project_root / "coverage.xml",
    ]
    for artifact in artifacts:
        _remove_path(artifact)

    for pycache_dir in _iter_pycache_dirs(project_root):
        _remove_path(pycache_dir)


def clean_external_cache(res_root: Path) -> None:
    cache_base = res_root / "cache" / "py-ia-rom-logger"
    targets = [
        cache_base,
        res_root / "cache" / "pycache",
    ]
    for target in targets:
        _remove_path(target)


def main() -> None:
    # Load .env if available
    project_root = Path(__file__).resolve().parents[2]
    env_file = project_root / ".env"
    if env_file.exists():
        try:
            from dotenv import load_dotenv
            load_dotenv(dotenv_path=env_file, override=False)
        except Exception:
            pass

    clean_local_artifacts(project_root)

    res_root_env = os.environ.get("RES_ROOT")
    if res_root_env:
        clean_external_cache(Path(res_root_env))


if __name__ == "__main__":
    main()


