from dataclasses import asdict, dataclass, field
from datetime import datetime
from getpass import getuser
from json import dumps as json_dumps
from platform import platform
from socket import gethostname
from typing import Any

from py_ia_rom_logger.config import SETTINGS


def now() -> datetime:
    return datetime.now(SETTINGS.TZ)


@dataclass
class SystemInfoHelper:
    """System information collector and holder.

    Captures and stores essential system metadata for logging context.

    Attributes:
        hostname: System hostname.
        username: Current user name.
        platform: Platform information string.
        timestamp: Current system datetime with configured timezone.
    """

    hostname: str = field(default_factory=gethostname)
    username: str = field(default_factory=getuser)
    platform: str = field(default_factory=platform)
    timestamp: datetime = field(default_factory=now)

    def __str__(self) -> str:
        return (
            f"SystemInfo("
            f"hostname='{self.hostname}', "
            f"username='{self.username}', "
            f"platform='{self.platform}', "
            f"timestamp='{self.timestamp.isoformat()}'"
            f")"
        )

    def __repr__(self) -> str:
        return self.__str__()

    @property
    def to_json(self) -> str:
        """Convert system information to JSON format.

        Returns:
            str: JSON representation of system info.
        """
        data_: dict[str, Any] = asdict(self)
        # 🔧 Implementation: Convert datetime to ISO string for JSON compatibility
        data_["timestamp"] = self.timestamp.isoformat()
        return json_dumps(data_, ensure_ascii=False, indent=2)
