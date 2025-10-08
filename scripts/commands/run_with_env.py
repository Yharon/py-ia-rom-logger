from __future__ import annotations

import os
import subprocess
import sys
from collections.abc import Sequence
from pathlib import Path


def _load_dotenv_if_present() -> None:
    try:
        from dotenv import load_dotenv
    except Exception:
        return
    project_root = Path(__file__).resolve().parents[2]
    env_file = project_root / ".env"
    if env_file.exists():
        load_dotenv(dotenv_path=env_file, override=False)


def _ensure_cache_env_from_res_root() -> None:
    res_root = os.environ.get("RES_ROOT")
    if not res_root:
        return
    base = Path(res_root) / "cache" / "py-ia-rom-logger"
    os.environ.setdefault("RUFF_CACHE_DIR", str(base / ".ruff_cache"))
    os.environ.setdefault("MYPY_CACHE_DIR", str(base / ".mypy_cache"))


def run_with_env(argv: Sequence[str] | None = None) -> int:
    _load_dotenv_if_present()
    _ensure_cache_env_from_res_root()

    args = list(sys.argv[1:] if argv is None else argv)
    if not args:
        print("No command provided.")
        return 2

    try:
        # Use shell=False for safety; allow quoted args
        proc = subprocess.run(args, check=False)
        return proc.returncode
    except FileNotFoundError as exc:
        print(f"Command not found: {args[0]} ({exc})")
        return 127


def main() -> None:
    sys.exit(run_with_env())


if __name__ == "__main__":
    main()



