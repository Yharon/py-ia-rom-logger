from dataclasses import asdict, dataclass, field
from json import dumps as json_dumps
from os import getenv
from pathlib import Path
from zoneinfo import ZoneInfo

from dotenv import load_dotenv

from . import PROJECT_ROOT
from .decorators import singleton


def get_prod_env_static() -> bool:
    """
    Verifica se o ambiente é de produção.
    """
    env_path: Path = Path(PROJECT_ROOT) / "configs" / ".env"
    if env_path.exists():
        load_dotenv(env_path)
        if getenv("ENV", "DEV").upper() != "PROD":
            return False
    return True


@singleton
def get_timezone() -> ZoneInfo:
    """
    Obtém o fuso horário configurado na variável de ambiente TIMEZONE.
    Se não estiver definido, usa o fuso horário padrão "America/Sao_Paulo".
    """
    tz_name: str = getenv("TIMEZONE", "America/Sao_Paulo")
    return ZoneInfo(tz_name)


@singleton
@dataclass
class Settings:
    """
    Classe de configurações do projeto.

    Centraliza todas as configurações e variáveis de ambiente
    necessárias para o funcionamento do sistema.
    """

    # Variáveis de ambiente
    PROJECT_ROOT_: Path = field(init=True)
    OS_WINDOWS: bool = field(init=True)
    PROD_ENV: bool = field(default_factory=get_prod_env_static)

    # Paths
    LOG_DIR: Path = field(init=False)

    # Data e hora
    TZ: ZoneInfo = field(init=False, default_factory=get_timezone)

    # Formatos de data e hora
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
        """
        Serializa as configurações para JSON.
        Converte os campos da classe em um dicionário e serializa
        para JSON, incluindo o fuso horário como string.
        Returns
        -------
        str
            Representação JSON das configurações.
        """
        data_ = asdict(self)

        data_["TZ"] = self.TZ.key
        return json_dumps(data_, ensure_ascii=False, indent=2)
