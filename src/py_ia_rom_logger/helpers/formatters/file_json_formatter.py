"""
Formatador JSON personalizado para logs RPA com sanitização e serialização segura.

Este módulo implementa um formatador JSON especializado para sistemas RPA que:
- Remove emojis e caracteres especiais dos logs
- Sanitiza placeholders de formatação Python (%s, %d, etc.)
- Converte objetos complexos em estruturas JSON-serializáveis
- Garante compatibilidade UTF-8 com sistemas terceiros
- Injeta argumentos customizados de forma estruturada

O formatador é especialmente útil para:
- Integração com sistemas de monitoramento externos
- Análise automatizada de logs RPA
- Armazenamento em bancos de dados JSON
- Transmissão de logs via APIs REST

Examples
--------
>>> from py_ia_rom_logger.helpers.formatters import SafeJsonFormatter
>>> import logging
>>>
>>> # Configuração básica
>>> formatter = SafeJsonFormatter()
>>> handler = logging.FileHandler('automation.log')
>>> handler.setFormatter(formatter)
>>>
>>> logger = logging.getLogger('rpa_automation')
>>> logger.addHandler(handler)
>>>
>>> # Log com argumentos complexos
>>> user_data = {'id': 123, 'name': 'João 😊'}
>>> logger.info("Processando usuário %s", user_data)
>>> # Resultado JSON: {"message": "Processando usuário", "customargs": {"id": 123, "name": "João"}}

Notes
-----
- Emojis são automaticamente removidos para compatibilidade com sistemas legados
- Placeholders Python (%s, %d, %(name)s) são extraídos da mensagem principal
- Argumentos de log são preservados no campo 'customargs' para análise posterior
- Objetos dataclass são automaticamente convertidos via asdict()
- Fallback seguro para objetos não-serializáveis usando repr()

See Also
--------
pythonjsonlogger.json.JsonFormatter : Classe base do formatador JSON
logging.Formatter : Interface padrão de formatação do Python
"""

from typing import Any

from pythonjsonlogger.json import JsonFormatter

from py_ia_rom_logger.models import FileLogModel

from .tracebacks.compact_traceback_formatter import CompactTracebackFormatter


class SafeJsonFormatter(JsonFormatter):
    """
    Formatador JSON especializado para logs de automação RPA.

    Este formatador estende o JsonFormatter padrão com funcionalidades
    específicas para ambientes RPA, incluindo:
    - Sanitização automática de emojis e caracteres especiais
    - Preservação de encoding UTF-8 para compatibilidade internacional
    - Separação de mensagem base e argumentos estruturados
    - Conversão segura de objetos complexos para JSON

    A classe é otimizada para integração com sistemas terceiros comuns
    em ambientes corporativos, garantindo compatibilidade e robustez.

    Attributes
    ----------
    _sanitize_str : method
        Método para sanitização de strings com remoção de emojis
    add_fields : method
        Override para injeção de campos customizados no log JSON

    Examples
    --------
    >>> import logging
    >>> from rpa_logger.helpers.formatters import SafeJsonFormatter
    >>>
    >>> # Configuração para arquivo de log
    >>> formatter = SafeJsonFormatter()
    >>> file_handler = logging.FileHandler('rpa_automation.json')
    >>> file_handler.setFormatter(formatter)
    >>>
    >>> logger = logging.getLogger('invoice_automation')
    >>> logger.addHandler(file_handler)
    >>>
    >>> # Exemplo de uso em automação
    >>> invoice_data = {
    ...     'id': 'INV-2024-001',
    ...     'amount': 1250.75,
    ...     'customer': 'Empresa ABC 🏢'
    ... }
    >>>
    >>> logger.info("Processando fatura %s no valor de R$ %.2f",
    ...              invoice_data['id'], invoice_data['amount'])
    >>>
    >>> # Resultado JSON estruturado:
    >>> # {
    >>> #   "asctime": "2024-01-15 14:30:25,123",
    >>> #   "levelname": "INFO",
    >>> #   "name": "invoice_automation",
    >>> #   "message": "Processando fatura no valor de R$",
    >>> #   "customargs": ["INV-2024-001", 1250.75]
    >>> # }

    Notes
    -----
    - Campo 'message' contém apenas texto base sem placeholders
    - Campo 'customargs' preserva argumentos originais de forma estruturada
    - Emojis são removidos automaticamente para compatibilidade de sistema
    - Encoding UTF-8 é garantido via backslash escape
    - Objetos complexos são convertidos de forma recursiva e segura

    See Also
    --------
    pythonjsonlogger.json.JsonFormatter : Classe base para formatação JSON
    logging.Formatter : Interface padrão do sistema de logging Python
    """

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._file_model = FileLogModel()
        self._tb_formatter = CompactTracebackFormatter(
            max_frames=kwargs.pop("max_frames", 8)
        )

    def _sanitize_str(self, txt_: str) -> str:
        """
        Sanitiza string removendo emojis e garantindo encoding UTF-8.

        Aplica dupla sanitização:
        1. Remove emojis e símbolos Unicode decorativos
        2. Força encoding UTF-8 com escape de caracteres problemáticos

        Parameters
        ----------
        txt : str
            String a ser sanitizada

        Returns
        -------
        str
            String sanitizada e com encoding UTF-8 garantido

        Examples
        --------
        >>> formatter = SafeJsonFormatter()
        >>> formatter._sanitize_str("Usuário João 😊 logado!")
        'Usuário João  logado!'

        >>> formatter._sanitize_str("Erro crítico ❌")
        'Erro crítico '
        """
        # Remove emojis primeiro
        txt: str = self._file_model.strip_emojis(txt_)
        # Garante encoding UTF-8 com escape de caracteres problemáticos
        return txt.encode("utf-8", "backslashreplace").decode("utf-8")

    def add_fields(self, log_record: dict, record: Any, message_dict: dict) -> None:
        """
        Adiciona campos customizados ao registro de log JSON.

        Override do método base para injetar funcionalidades RPA:
        - Limpa placeholders da mensagem principal
        - Injeta argumentos estruturados em campo separado
        - Sanitiza todas as strings presentes no log

        Parameters
        ----------
        log_record : dict
            Dicionário do registro de log sendo construído
        record : LogRecord
            Objeto LogRecord original do Python logging
        message_dict : dict
            Dicionário de mensagens formatadas

        Notes
        -----
        Este método é chamado automaticamente pelo JsonFormatter
        durante o processo de formatação do log. Não deve ser
        chamado diretamente pelo código cliente.

        Examples
        --------
        # Comportamento interno do método:
        # Input LogRecord: msg="Usuário %s processado", args=("João",)
        # Output log_record: {
        #   "message": "Usuário  processado",
        #   "customargs": "João",
        #   ...outros campos...
        # }
        """
        # Preenche campos padrão usando implementação base
        super().add_fields(log_record, record, message_dict)

        # Sobrescreve 'message' removendo placeholders de formatação
        raw_msg = str(getattr(record, "msg", ""))
        log_record["message"] = self._sanitize_str(
            self._file_model.remove_placeholders(raw_msg)
        )

        # Injeta 'customargs' se existirem argumentos de formatação
        if record.args:
            # Para argumentos únicos, extrai do tuple para facilitar parsing
            payload = (
                self._file_model.jsonable(record.args[0])
                if isinstance(record.args, tuple) and len(record.args) == 1
                else self._file_model.jsonable(record.args)
            )
            log_record["customargs"] = payload

        if record.exc_info:
            tb_str, exc_name, exc_msg = self._tb_formatter.format(record.exc_info)

            log_record["exc_info"] = self._sanitize_str(tb_str)
            log_record["exc_name"] = self._sanitize_str(exc_name)
            log_record["exc_message"] = self._sanitize_str(exc_msg)
