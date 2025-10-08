from linecache import getline
import traceback as tb_module
from pathlib import Path
from datetime import datetime
from types import TracebackType

from rich.text import Text

from py_ia_rom_logger.config import SETTINGS


def truncate_string(s, max_length=100):
    if len(s) > max_length:
        return s[: max_length - 4] + " ..."
    return s


class TracebackRichFormatter:
    """
    Formatter Rich com traceback em formato de tabela.

    Apresenta o traceback em uma tabela estruturada
    para melhor visualização das informações.
    """

    _traceback_lines: list[str]
    _tb_list: tb_module.StackSummary
    _last_frames: list[tb_module.FrameSummary]

    _exc_title = (
        Text()
        .append("🐛 ", style="bold")
        .append("DEBUG", style="bold yellow")
        .append("INFO - ", style="bold red")
        .append(
            datetime.now(SETTINGS.TZ).strftime(SETTINGS.TIMESTAMP_FORMAT),
            style="bold white",
        )
    )

    def create_rich_traceback(
        self,
        exc_type: type[BaseException],
        exc_value: BaseException,
        exc_traceback: TracebackType | None,
    ) -> str:
        """
        Cria traceback em formato de tabela.

        Parameters
        ----------
        exc_type : type[BaseException]
            Tipo da exceção
        exc_value : BaseException
            Valor da exceção
        exc_traceback : TracebackType | None
            Traceback da exceção, pode ser None se não houver traceback

        Returns
        -------
        str
            Traceback formatado como string
        """

        self._configs(exc_traceback)

        self._cabecalho()

        self._formata_frames()

        self._format_exc_msg(exc_type, exc_value)

        return "\n".join(self._traceback_lines)

    def _format_exc_msg(
        self, exc_type: type[BaseException], exc_value: BaseException
    ) -> None:
        """
        Formata a mensagem de exceção.

        Parameters
        ----------
        exc_type : type[BaseException]
            Tipo da exceção
        exc_value : BaseException
            Valor da exceção
        """
        exc_name = exc_type.__name__
        exc_message = str(exc_value)

        self._traceback_lines.append(
            Text(f"\n🚨 {exc_name}: ", style="bold red").markup
        )
        self._traceback_lines.append(
            Text(f"    {str(exc_message)}", style="yellow").markup
        )

    def _configs(self, exc_traceback: TracebackType | None) -> None:
        """
        Configurações iniciais do traceback.
        Define o estilo e outras configurações necessárias.
        """
        self._traceback_lines = []

        self._tb_list = tb_module.extract_tb(exc_traceback)
        self._last_frames = (
            self._tb_list[-SETTINGS.TRACEBACKS_MAX_FRAMES :] if self._tb_list else []
        )

    def _cabecalho(self) -> None:
        """
        Adiciona o cabeçalho do traceback.
        """
        self._traceback_lines.append("")

    def _formata_frames(self) -> None:
        """
        Formata os frames do traceback.
        """
        for i, frame in enumerate(self._last_frames):
            self._info_file(frame)
            self._info_lines(frame, i)

    def _info_lines(self, frame: tb_module.FrameSummary, frame_num: int) -> None:
        """
        Obtém informações da linha do frame.

        Parameters
        ----------
        frame : tb_module.FrameSummary
            Frame do traceback

        Returns
        -------
        str
            Informações formatadas da linha
        """

        if frame.line and frame.lineno:
            lineno = frame.lineno

            if frame_num == len(self._last_frames) - 1:
                self._format_frame_lines(frame, lineno)
            else:
                self._format_frame_func(frame)

    def _format_frame_func(self, frame: tb_module.FrameSummary) -> None:
        """
        Formata a função do frame.

        Parameters
        ----------
        frame : tb_module.FrameSummary
            Frame do traceback
        """

        self._traceback_lines.append(
            f'{Text("    in", style="dim").markup} '
            f'{Text(frame.name, style="green").markup}'
        )

    def _format_frame_lines(self, frame: tb_module.FrameSummary, lineno: int) -> None:
        """
        Formata as linhas do frame com contexto.

        Parameters
        ----------
        frame : tb_module.FrameSummary
            Frame do traceback
        """
        context = SETTINGS.TRACEBACKS_CONTEXT_LINES
        start = max(1, lineno - context)
        end = lineno + context

        for i in range(start, end + 1):
            line = getline(frame.filename, i).rstrip()
            formatted_line = self._format_indentation(line)
            if i == lineno:
                self._traceback_lines.append(
                    Text(
                        truncate_string(f"👀{i:4d}: {formatted_line}"),
                        style="bold white on red",
                    ).markup
                )
            else:
                self._traceback_lines.append(
                    truncate_string(f"  {i:4d}: {formatted_line}")
                )

    def _format_indentation(self, line: str) -> str:
        """
        Formata a indentação do frame.

        Parameters
        ----------
        line : str
            Linha do frame a ser formatada
        Returns
        -------
        str
            Linha formatada com a indentação correta
        """
        INDENT_SPACES = 4

        # Calcula os espaços de indentação
        leading_spaces = len(line) - len(line.lstrip(" "))

        # Calcula quantos grupos de indentação existem e os espaços restantes
        groups = leading_spaces // INDENT_SPACES
        leftover = leading_spaces % INDENT_SPACES

        # Para cada grupo, substitui '    ' por '│   '
        vertical_indent = ("│" + " " * (INDENT_SPACES - 1)) * groups + " " * leftover

        # Concatena a indentação modificada com o restante da linha (sem os espaços à esquerda originais)
        return vertical_indent + line.lstrip().rstrip()

    def _info_file(self, frame: tb_module.FrameSummary) -> None:
        """
        Obtém informações do arquivo do frame e adiciona ao traceback.

        Parameters
        ----------
        frame : tb_module.FrameSummary
            Frame do traceback
        """
        file_path = Path(frame.filename)
        filename = file_path.name
        directory = (
            file_path.parent.name
            if file_path.parent.name != file_path.parent.anchor
            else ""
        )
        self._traceback_lines.append(
            f'📁 {directory}/{filename}{Text(":", style="dim").markup}'
            f'{Text(str(frame.lineno), style="magenta").markup}'
        )

    @property
    def exc_title(self) -> str:
        """
        Obtém o título da exceção formatado.

        Returns
        -------
        str
            Título da exceção formatado com Rich markup
        """
        return self._exc_title.markup
