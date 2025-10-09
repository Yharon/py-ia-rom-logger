from os import name as os_name
from sys import path as sys_path
from pathlib import Path


PROJECT_ROOT = str(Path.cwd())
if PROJECT_ROOT not in sys_path:
    sys_path.insert(0, PROJECT_ROOT)

if os_name == "nt":  # nt = Windows
    OS_WINDOWS = True
elif os_name == "posix":  # posix = Linux/Mac
    OS_WINDOWS = False
else:
    raise RuntimeError(f"Unsupported OS: {os_name}")


from .config import Settings


# 🏗️ Architecture: Global singleton instance of settings
SETTINGS = Settings(PROJECT_ROOT_=Path(PROJECT_ROOT), OS_WINDOWS=OS_WINDOWS)

__all__ = [
    "SETTINGS",
    "OS_WINDOWS"
]
