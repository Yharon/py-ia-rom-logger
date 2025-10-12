# from os import getenv
from os import name as os_name
from pathlib import Path
from sys import path as sys_path


PROJECT_ROOT = str(Path.cwd())
if PROJECT_ROOT not in sys_path:
    sys_path.insert(0, PROJECT_ROOT)


if os_name == "nt":  # nt = Windows
    OS_WINDOWS = True
elif os_name == "posix":  # posix = Linux/Mac
    OS_WINDOWS = False
else:
    raise RuntimeError(f"Unsupported OS: {os_name}")


from .config import Settings  # noqa: E402


# def print_debug_info() -> None:
#     """Print debug information about paths and environment variables.

#     This function is called automatically when DEBUG_PRINT_VARS=1 is set.
#     It prints all important configuration variables BEFORE the debugger connects.
#     """
#     print("\n" + "="*80)
#     print("🐛 DEBUG INFO - Configuration Variables")
#     print("="*80)

#     # Current working directory
#     print(f"\n📂 Current Working Directory:")
#     print(f"   Path.cwd() = {Path.cwd()}")

#     # Project root
#     print(f"\n📁 Project Root:")
#     print(f"   PROJECT_ROOT = {PROJECT_ROOT}")

#     # Environment variables
#     print(f"\n🌍 Environment Variables:")
#     print(f"   ENV = {getenv('ENV', 'NOT SET')}")
#     print(f"   LOG_DIR = {getenv('LOG_DIR', 'NOT SET (will use default)')}")
#     print(f"   ROBO_ID = {getenv('ROBO_ID', 'NOT SET')}")
#     print(f"   ROUND_ID = {getenv('ROUND_ID', 'NOT SET')}")
#     print(f"   TIMEZONE = {getenv('TIMEZONE', 'NOT SET')}")
#     print(f"   TRACEBACKS_MAX_FRAMES = {getenv('TRACEBACKS_MAX_FRAMES', 'NOT SET')}")
#     print(f"   TRACEBACKS_EXTRA_LINES = {getenv('TRACEBACKS_EXTRA_LINES', 'NOT SET')}")
#     print(f"   TRACEBACKS_CONTEXT_LINES = {getenv('TRACEBACKS_CONTEXT_LINES', 'NOT SET')}")

#     # Cache-related environment variables
#     print(f"\n💾 Cache Environment Variables:")
#     print(f"   PYTHONPYCACHEPREFIX = {getenv('PYTHONPYCACHEPREFIX', 'NOT SET')}")
#     print(f"   CACHE_DIR = {getenv('CACHE_DIR', 'NOT SET')}")
#     print(f"   PYTEST_CACHE_DIR = {getenv('PYTEST_CACHE_DIR', 'NOT SET')}")
#     print(f"   MYPY_CACHE_DIR = {getenv('MYPY_CACHE_DIR', 'NOT SET')}")
#     print(f"   RUFF_CACHE_DIR = {getenv('RUFF_CACHE_DIR', 'NOT SET')}")

#     print("\n" + "="*80 + "\n")

# # 🏗️ Architecture: Global singleton instance of settings
SETTINGS = Settings(PROJECT_ROOT_=Path(PROJECT_ROOT), OS_WINDOWS=OS_WINDOWS)


# # 🐛 Debug: Print debug info if DEBUG_PRINT_VARS is set
# if getenv("DEBUG_PRINT_VARS", "0") == "1":
#     print_debug_info()
#     print("⚙️  Settings Configuration:")
#     print(f"   SETTINGS.PROJECT_ROOT_ = {SETTINGS.PROJECT_ROOT_}")
#     print(f"   SETTINGS.LOG_DIR = {SETTINGS.LOG_DIR}")
#     print(f"   SETTINGS.PROD_ENV = {SETTINGS.PROD_ENV}")
#     print(f"   SETTINGS.OS_WINDOWS = {SETTINGS.OS_WINDOWS}")
#     print(f"   SETTINGS.TZ = {SETTINGS.TZ.key}")
#     print(f"   SETTINGS.ROBO_ID = {SETTINGS.ROBO_ID}")
#     print(f"   SETTINGS.ROUND_ID = {SETTINGS.ROUND_ID}")
#     print(f"   SETTINGS.MAX_FILES = {SETTINGS.MAX_FILES}")
#     print("\n" + "="*80)
#     print("✅ Debug info printed - Ready to connect debugger!")
#     print("="*80 + "\n")


__all__ = [
    "OS_WINDOWS",
    "SETTINGS"
]
