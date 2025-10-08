from dataclasses import asdict, dataclass, field
from json import dumps as json_dumps
from os import getenv
from pathlib import Path
from zoneinfo import ZoneInfo

from dotenv import load_dotenv

from . import PROJECT_ROOT
from .decorators import singleton


def get_prod_env_static() -> bool:
    """Check if the current environment is production.

    Returns:
        bool: True if ENV='PROD' in .env file, False otherwise.
    """
    env_path: Path = Path(PROJECT_ROOT) / "configs" / ".env"
    if env_path.exists():
        load_dotenv(env_path)
        if getenv("ENV", "DEV").upper() != "PROD":
            return False
    return True


@singleton
def get_timezone() -> ZoneInfo:
    """Get the configured timezone from environment variable.

    Returns:
        ZoneInfo: Timezone from TIMEZONE env var, defaults to 'America/Sao_Paulo'.
    """
    tz_name: str = getenv("TIMEZONE", "America/Sao_Paulo")
    return ZoneInfo(tz_name)


@singleton
@dataclass
class Settings:
    """Application configuration settings.

    Centralizes all configuration and environment variables needed
    for the system to function properly.

    Attributes:
        PROJECT_ROOT_: Root directory path of the project.
        OS_WINDOWS: True if running on Windows, False otherwise.
        PROD_ENV: True if environment is production.
        LOG_DIR: Directory path for log files.
        TZ: Configured timezone.
        TIMESTAMP_FORMAT: Time format for log timestamps.
        MAX_FILES: Maximum number of backup log files to keep.
        ROBO_ID: Robot identifier from environment.
        ROUND_ID: Round identifier from environment.
        TRACEBACKS_MAX_FRAMES: Maximum frames to show in tracebacks.
        TRACEBACKS_EXTRA_LINES: Extra context lines around traceback.
        TRACEBACKS_CONTEXT_LINES: Context lines for each frame.
    """

    # Environment variables
    PROJECT_ROOT_: Path = field(init=True)
    OS_WINDOWS: bool = field(init=True)
    PROD_ENV: bool = field(default_factory=get_prod_env_static)

    # Paths
    LOG_DIR: Path = field(init=False)

    # Date and time
    TZ: ZoneInfo = field(init=False, default_factory=get_timezone)

    # Date and time formats
    TIMESTAMP_FORMAT: str = field(init=False, default="%H:%M:%S")

    MAX_FILES: int = field(init=False, default=5)
    ROBO_ID: str = field(init=False, default_factory=lambda: getenv("ROBO_ID", "1"))
    ROUND_ID: str = field(init=False, default_factory=lambda: getenv("ROUND_ID", "01"))
    TRACEBACKS_MAX_FRAMES: int = field(init=False, default_factory=lambda: int(getenv("TRACEBACKS_MAX_FRAMES", "8")))
    TRACEBACKS_EXTRA_LINES: int = field(init=False, default_factory=lambda: int(getenv("TRACEBACKS_EXTRA_LINES", "3")))
    TRACEBACKS_CONTEXT_LINES: int = field(
        init=False, default_factory=lambda: int(getenv("TRACEBACKS_CONTEXT_LINES", "3"))
    )

    def __post_init__(self):

        self.LOG_DIR = Path(getenv("LOG_DIR", self.PROJECT_ROOT_ / "logs"))

        if not self.LOG_DIR.exists():
            self.LOG_DIR.mkdir(parents=True, exist_ok=True)

    def __str__(self):
        return (
            f"Settings("
            f"PROD_ENV={self.PROD_ENV}, "
            f"LOG_DIR='{self.LOG_DIR}', "
            f"TZ='{self.TZ.key}'"
            ")"
        )

    def __repr__(self):
        return self.__str__()

    @property
    def to_json(self) -> str:
        """Serialize settings to JSON format.

        Returns:
            str: JSON representation of all settings.
        """
        data_ = asdict(self)
        # 🔧 Implementation: Convert ZoneInfo to string for JSON serialization
        data_["TZ"] = self.TZ.key
        return json_dumps(data_, ensure_ascii=False, indent=2)
