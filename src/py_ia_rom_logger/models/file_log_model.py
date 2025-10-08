from re import compile as re_compile, UNICODE as re_UNICODE, Pattern as re_Pattern
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from py_ia_rom_logger.config import SETTINGS

from . import LogModel


@dataclass
class FileLogModel(LogModel):
    """
    Modelo de log para saída em arquivos.

    Este modelo estende LogModel para fornecer funcionalidades específicas
    para logs em arquivos, incluindo formatação de nomes de arquivos e
    gerenciamento de backups.

    Attributes
    ----------
    _robo_id : str
        Identificador do robô, usado para nomear arquivos de log.
    _part_01 : str
        Parte fixa do nome do arquivo de log, geralmente um prefixo.
    _nome_completo : str
        Nome completo do arquivo de log, composto pelo robo_id e part_01.
    BACKUP_LOG_NAME : str
        Nome do arquivo de log de backup.
    FORMAT_DATE_NAME : str
        Formato de data usado nos nomes dos arquivos de log.
    FORMAT_TIME_NAME : str
        Formato de hora usado nos nomes dos arquivos de log.
    _EMOJI_RE : re.Pattern
        Expressão regular para remover emojis e caracteres especiais
        de mensagens de log, garantindo compatibilidade com sistemas legados.

    Methods
    -------
    create_log_file_name(date_: Optional[datetime] = None) -> str
        Cria o nome do arquivo de log com base no formato definido.
    strip_emojis(text: str) -> str
        Remove emojis e símbolos Unicode decorativos do texto,
    """

    _robo_id = SETTINGS.ROBO_ID
    _part_01 = "01"
    _nome_completo: str = field(init=False, default=f"{_robo_id}_{_part_01}")

    BACKUP_LOG_NAME: str = field(init=False, default=_nome_completo)
    FORMAT_DATE_NAME: str = field(init=False, default="%Y%m%d")
    FORMAT_TIME_NAME: str = field(init=False, default="%H%M%S")

    _EMOJI_RE: re_Pattern = field(
        init=False,
        default=re_compile(
            "["  # início do conjunto de caracteres
            "\U0001f600-\U0001f64f"  # emoticons (rostos e gestos)
            "\U0001f300-\U0001f5ff"  # símbolos & pictogramas diversos
            "\U0001f680-\U0001f6ff"  # transporte e símbolos de mapa
            "\U0001f1e0-\U0001f1ff"  # bandeiras (regional indicator symbols)
            "\u2600-\u26ff"  # símbolos diversos (weather, zodiac, etc.)
            "\u2700-\u27bf"  # dingbats (decorative symbols)
            "]+",
            flags=re_UNICODE,
        ),
    )

    def create_log_file_name(self, date_: Optional[datetime] = None) -> str:
        """
        Cria o nome do arquivo de log com base no formato definido.

        Returns
        -------
        str
            Nome do arquivo de log formatado.
        """
        if date_ is None:
            date_ = datetime.now(SETTINGS.TZ)

        name = self._nome_completo
        date_name = date_.strftime(self.FORMAT_DATE_NAME)
        hour_name = date_.strftime(self.FORMAT_TIME_NAME)
        round_id = SETTINGS.ROUND_ID

        return f"{name}_{date_name}_{hour_name}_{round_id}.log"

    def strip_emojis(self, text: str) -> str:
        """
        Remove emojis e símbolos Unicode decorativos do texto.

        Função essencial para RPA que integra com sistemas legados
        que não suportam emojis ou caracteres Unicode especiais.

        Parameters
        ----------
        text : str
            Texto a ser sanitizado

        Returns
        -------
        str
            Texto sem emojis, ou string vazia se input for None/vazio

        Examples
        --------
        >>> _strip_emojis("Usuário processado com sucesso! 😊✅")
        'Usuário processado com sucesso! '

        >>> _strip_emojis("Erro crítico ❌🚨")
        'Erro crítico '
        """
        return self._EMOJI_RE.sub("", text) if text else ""
