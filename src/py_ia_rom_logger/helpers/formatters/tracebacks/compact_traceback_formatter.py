"""
CompactTracebackFormatter
-------------------------

Gera uma representação enxuta do traceback para ser gravada em JSON,
limitando o número de quadros e exibindo apenas:

    caminho/relativo.py:linha  in funcao
    [...]
    caminho/relativo.py:linha  "código fonte"

Exemplo padrão (max_frames=8):

use_examples/basic_usage.py:88 in uso_basico_rpa_logger
use_examples/basic_usage.py:46 in funcao_nivel_1
use_examples/basic_usage.py:55  "resultado = 10 / 0"
"""

from __future__ import annotations

import os
import traceback
from typing import List, Tuple


class CompactTracebackFormatter:
    """Formata traceback de forma resumida.

    Parameters
    ----------
    max_frames : int, default 8
        Número máximo de quadros que serão incluídos (contando de baixo para cima).
    base_dir : str | None
        Diretório base para tornar caminhos relativos.
        Se None, usa ``os.getcwd()``.
    """

    def __init__(self, max_frames: int = 8, base_dir: str | None = None) -> None:
        self.max_frames = max_frames
        self.base_dir = base_dir or os.getcwd()

    # --------------------------------------------------------------------- #
    # API pública
    # --------------------------------------------------------------------- #
    def format(self, exc_info) -> Tuple[str, str, str]:
        """
        Recebe ``exc_info`` (``sys.exc_info()``) e devolve:

        Returns
        -------
        traceback_str : str
            Traceback formatado, linhas separadas por ``\n `` (note o espaço).
        exc_name : str
            Nome da exceção (ex.: ``ZeroDivisionError``).
        exc_msg : str
            Mensagem/descrição da exceção.
        """
        exc_type, exc_val, tb = exc_info
        exc_name = exc_type.__name__ if exc_type else ""
        exc_msg = str(exc_val) if exc_val else ""

        frames = traceback.extract_tb(tb)
        # pega apenas os últimos N quadros (caminho ascendente até a origem)
        frames = frames[-self.max_frames :] if self.max_frames else frames

        formatted: List[str] = []
        for filename, lineno, func, text in frames[:-1]:
            rel = os.path.relpath(filename, self.base_dir)
            formatted.append(f"{rel}:{lineno} in {func}")

        # último quadro → inclui linha de código
        if frames:
            filename, lineno, func, text = frames[-1]
            rel = os.path.relpath(filename, self.base_dir)
            code = (text or "").strip().replace('"', r"\"").replace("'", r"\'")
            formatted.append(f'{rel}:{lineno}  "{code}"')

        traceback_str = "\n ".join(formatted)
        return traceback_str, exc_name, exc_msg
