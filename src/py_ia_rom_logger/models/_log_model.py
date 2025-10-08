from re import compile as re_compile, VERBOSE as re_VERBOSE, Pattern as re_Pattern
from functools import cached_property
from dataclasses import dataclass, field, is_dataclass, asdict as dataclasses_asdict
from typing import Any, Mapping, Sequence

from rich.theme import Theme


@dataclass
class LogModel:
    """
    Modelo de log base para outros modelos de log

    Este modelo define a estrutura básica de um log, incluindo
    níveis de log, regex para placeholders e um mapeamento de níveis.

    Attributes
    ----------
    LOG_LEVELS : tuple
        Tupla de níveis de log suportados, na ordem de prioridade.
    _PLACEHOLDER_RE : re.Pattern
        Expressão regular para identificar e remover placeholders de formatação. Remove
        placeholders como %s, %d, %.2f, %10s, %(name)s, etc.
    """

    LOG_LEVELS: tuple = field(
        init=False,
        default=(
            "DEBUG",
            "INFO",
            "WARNING",
            "ERROR",
            "CRITICAL",
        ),
    )

    _PLACEHOLDER_RE: re_Pattern = field(
        init=False,
        default=re_compile(
            r"""
                %                       # inicia com símbolo de placeholder
                (?:\([^)]+\))?          # opcional: placeholder nomeado %(name)s
                [-+#0\s]*               # flags de formatação (alinhamento, padding)
                (?:\d+|\*)?             # largura do campo (número ou asterisco)
                (?:\.(?:\d+|\*))?       # precisão decimal (para floats)
                [bcdeEfFgGnosxXrs%]     # especificador de tipo final
            """,
            re_VERBOSE,
        ),
    )

    @cached_property
    def level_map(self):
        return dict(map(lambda k: (k, k[:4]), self.LOG_LEVELS))

    def remove_placeholders(self, text: str) -> str:
        """
        Remove placeholders de formatação Python da mensagem de log.

        Extrai placeholders como %s, %d, %(field)s da mensagem principal,
        mantendo apenas o texto base. Os valores dos placeholders são
        preservados separadamente no campo 'customargs'.

        Parameters
        ----------
        text : str
            Mensagem de log com placeholders

        Returns
        -------
        str
            Mensagem limpa sem placeholders, com espaços extras removidos

        Examples
        --------
        >>> _remove_placeholders("Processando usuário %s com ID %d")
        'Processando usuário com ID'

        >>> _remove_placeholders("Erro no campo %(field_name)s: %.2f%%")
        'Erro no campo:'

        >>> _remove_placeholders("Status: %s | Progresso: %d de %d")
        'Status: | Progresso: de'
        """
        return self._PLACEHOLDER_RE.sub("", text).strip()

    def jsonable(self, value, *, _seen: set[int] | None = None) -> Any:
        """
        Converte objetos Python em estruturas serializáveis para JSON.

        Implementa estratégia em cascata para lidar com diferentes tipos
        de objetos encontrados em automações RPA, priorizando:
        1. Tipos primitivos (já JSON-compatíveis)
        2. Containers básicos (dict, list, tuple)
        3. Dataclasses (conversão via asdict)
        4. Objetos com __repr__ personalizado
        5. Objetos com método to_dict()
        6. Objetos com atributo __dict__
        7. Fallback para representação string

        Parameters
        ----------
        value : Any
            Objeto a ser convertido para formato JSON-compatível

        Returns
        -------
        Any
            Versão JSON-serializável do objeto original

        Examples
        --------
        >>> from dataclasses import dataclass
        >>> @dataclass
        ... class User:
        ...     name: str
        ...     age: int
        >>>
        >>> user = User("João", 30)
        >>> _jsonable(user)
        {'name': 'João', 'age': 30}

        >>> _jsonable({"status": "success", "items": [1, 2, 3]})
        {'status': 'success', 'items': [1, 2, 3]}

        >>> class CustomObject:
        ...     def __init__(self, value):
        ...         self.value = value
        ...     def __repr__(self):
        ...         return f"CustomObject({self.value})"
        >>>
        >>> _jsonable(CustomObject("test"))
        'CustomObject(test)'

        Notes
        -----
        - Preserva estrutura original de containers (dict/list)
        - Dataclasses são automaticamente convertidos via dataclasses.asdict()
        - Objetos com __repr__ customizado são convertidos para string
        - Fallback seguro evita falhas de serialização em produção
        """
        if _seen is None:
            _seen = set()
        obj_id = id(value)
        if obj_id in _seen:  # evita ciclos
            return str(value)
        _seen.add(obj_id)

        # 1) primitivos
        if value is None or isinstance(value, (str, int, float, bool)):
            return value

        # 2) dataclass
        if is_dataclass(value) and not isinstance(value, type):
            return {
                k: self.jsonable(v, _seen=_seen)
                for k, v in dataclasses_asdict(value).items()
            }

        # 3) containers – RECURSIVO
        if isinstance(value, Mapping):
            return {k: self.jsonable(v, _seen=_seen) for k, v in value.items()}

        if isinstance(value, Sequence) and not isinstance(
            value, (str, bytes, bytearray)
        ):
            return [self.jsonable(v, _seen=_seen) for v in value]

        # 4) repr prioritário
        if type(value).__repr__ is not object.__repr__:
            return str(value)

        # 5) to_dict()
        to_dict = getattr(value, "to_dict", None)
        if callable(to_dict):
            try:
                return self.jsonable(to_dict(), _seen=_seen)
            except Exception:
                pass

        # 6) __dict__
        if hasattr(value, "__dict__"):
            return {k: self.jsonable(v, _seen=_seen) for k, v in vars(value).items()}

        # 7) fallback
        return str(value)


@dataclass
class CustomThemes:
    """
    Temas personalizados para o logger.
    """

    DEFAULT: Theme = field(
        init=False,
        default_factory=lambda: Theme(
            {
                "debug": "blue",
                "info": "green",
                "warning": "yellow",
                "error": "red",
                "critical": "bold red",
                "traceback": "dim bright_red",
            }
        ),
    )

    RICH: Theme = field(
        init=False,
        default_factory=lambda: Theme(
            {  # DEBUG: ambos apagados
                "logging.level.DEBUG": "gray35",
                "logging.message.DEBUG": "bright_black",
                # INFO: ambos verdes, level escuro, mensagem viva
                "logging.level.INFO": "green3",
                "logging.message.INFO": "green4",
                # WARNING: ambos amarelos, level escuro, mensagem viva
                "logging.level.WARNING": "bold white on yellow3",
                "logging.message.WARNING": "yellow2",
                # ERROR: ambos vermelhos, level escuro, mensagem viva
                "logging.level.ERROR": "bright_red",
                "logging.message.ERROR": "red3",
                # CRITICAL: ambos vermelhos, level escuro/fundo, mensagem viva/forte
                "logging.level.CRITICAL": "bold white on bright_red",
                "logging.message.CRITICAL": "bold white on red3",
                # Estilos para traceback
                "traceback.code": "dim white",
                "traceback.locals": "dim blue",
            }
        ),
    )
