"""
Exemplo básico de uso do RPA Custom Logger
Demonstra todas as funcionalidades implementadas na Fase 1
"""
from logging import getLogger, info, debug, warning, error, critical, exception
from dataclasses import dataclass, field as dc_field

from simple_parsing import field
from py_ia_rom_logger import LoggingManager
from py_clean_cli import command, CommandArgsModel


LOGGING_MANAGER  = LoggingManager()
LOGGER = getLogger(__name__)

@command(name="basic", help_text="Demonstração de uso básico.")
@dataclass
class BasicCommand(CommandArgsModel):
    """Configurações básicas para operações de logging."""

    destination_file: str = dc_field(
        default="logs",
        metadata=dict(help="Diretório do arquivo de log.", required=False),
        kw_only=True,
    )

    def exec(self) -> None:
        """
        Implementação do comando básico
        """
        if self.verbose:
            level = "DEBUG"
        else:
            level = "INFO"
        LOGGING_MANAGER.setup_logging(level=level)

        uso_basico_rpa_logger()
        if self.verbose:
            erro_nao_capturado()

class CustomException(Exception):
    """
    Exceção personalizada para o RPA Logger.
    Pode ser usada para capturar erros específicos de automação.
    """


class CustomModel:
    """
    Modelo personalizado para o RPA Logger.
    Pode ser usado para definir estruturas de dados específicas.
    """

    def __init__(self, name: str, value: int = 10):
        self.name = name
        self.value = value

    def __str__(self):
        return f"CustomModel(name={self.name}, value={self.value})"

    def __repr__(self):
        return self.__str__()

    def to_dict(self):
        """
        Converte o modelo personalizado em um dicionário.
        Pode ser usado para serialização ou formatação de logs.
        """
        return {"name": self.name, "value": self.value}


def funcao_nivel_1():
    funcao_nivel_2()


def funcao_nivel_2():
    funcao_nivel_3()


def funcao_nivel_3():
    # Simula erro de automação
    resultado = str(10 / 0)
    return resultado


def uso_basico_rpa_logger():
    """
    Demonstra o uso básico do RPA Logger
    """
    modelos = [
        CustomModel("Modelo 1"),
        CustomModel("Modelo 2"),
        CustomModel("Modelo 3"),
    ]
    dict_ = {
        "modelos": modelos,
        "descricao": "Exemplo de uso do RPA Logger com modelos personalizados",
    }
    print("=== Exemplo 1 Básico de Uso do RPA Logger ===")
    print("Deveria mostrar logs com cores e formatação personalizada\n")
    info(
        "Processo iniciado com sucesso! 🚀✨ %s%s%s",
        CustomModel("Modelo 1"),
        CustomModel("Modelo 2").to_dict(),
        "🥳🥳",
    )
    info("Processo iniciado com sucesso! 🚀✨ %s", CustomModel("Modelo 1"))
    debug("Este é um log de depuração (DEBUG) %s", dict_)
    warning("Este é um log de aviso (WARNING)")
    error("Este é um log de erro (ERROR)")
    critical("Este é um log crítico (CRITICAL)")

    try:
        # Simulando uma exceção
        funcao_nivel_1()
    except ZeroDivisionError:
        # raise CustomException("Erro de divisão por zero na função funcao_nivel_3")
        exception(
            "Este é um log de exceção (EXCEPTION) %s", CustomModel("Modelo 3").to_dict()
        )


def erro_nao_capturado():
    """
    Função que gera um erro não capturado para demonstrar o log de exceção
    """
    # Simula erro de automação
    resultado = 10 / 0
    return resultado
