from dataclasses import dataclass, field, asdict
from datetime import datetime
from platform import platform
from socket import gethostname
from getpass import getuser
from json import dumps as json_dumps

from py_ia_rom_logger.config import SETTINGS


def now():
    return datetime.now(SETTINGS.TZ)


@dataclass
class SystemInfoHelper:
    """
    Classe responsável por coletar e armazenar informações do sistema.
    Atributos:
        hostname (str): Nome do host do sistema.
        username (str): Nome do usuário atual.
        platform (str): Informações da plataforma do sistema.
        timestamp (datetime): Data e hora atual do sistema.
    """

    hostname: str = field(default_factory=gethostname)
    username: str = field(default_factory=getuser)
    platform: str = field(default_factory=platform)
    timestamp: datetime = field(default_factory=now)

    def __str__(self):
        return (
            f"SystemInfo("
            f"hostname='{self.hostname}', "
            f"username='{self.username}', "
            f"platform='{self.platform}', "
            f"timestamp='{self.timestamp.isoformat()}'"
            f")"
        )

    def __repr__(self):
        return self.__str__()

    @property
    def to_json(self) -> str:
        """Converte as informações do sistema para JSON.
        Returns
        -------
        str
            Representação JSON das informações do sistema.
        """
        data_ = asdict(self)
        # timestamp is not serializable, convert manually
        data_["timestamp"] = self.timestamp.isoformat()
        return json_dumps(data_, ensure_ascii=False, indent=2)
