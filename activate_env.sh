#!/bin/bash
# activate_env.sh - Script de ativação do ambiente py-ia-rom-logger
# Uso: source activate_env.sh

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Verificar se RES_ENVS e RES_ROOT estão definidos
if [ -z "$RES_ENVS" ] || [ -z "$RES_ROOT" ]; then
    echo -e "${YELLOW}⚠ Variáveis RES_ENVS ou RES_ROOT não definidas${NC}"
    echo "Defina-as no seu ~/.bashrc ou ~/.zshrc"
    return 1
fi

# Ativar virtual environment
VENV_PATH="$RES_ENVS/py-ia-rom-logger-venv/.venv"
if [ ! -d "$VENV_PATH" ]; then
    echo -e "${YELLOW}⚠ Virtual environment não encontrado: $VENV_PATH${NC}"
    return 1
fi

source "$VENV_PATH/bin/activate"

# Criar diretório de cache externo se não existir
CACHE_DIR="$RES_ROOT/cache/py-ia-rom-logger"
mkdir -p "$CACHE_DIR"
mkdir -p "$CACHE_DIR/pycache"
mkdir -p "$CACHE_DIR/htmlcov"
mkdir -p "$CACHE_DIR/.pytest_cache"
mkdir -p "$CACHE_DIR/.mypy_cache"
mkdir -p "$CACHE_DIR/.ruff_cache"

# Criar symlinks para cache (se não existirem)
# Usar -f para forçar sobrescrita de links antigos
ln -sf "$CACHE_DIR/.pytest_cache" .pytest_cache
ln -sf "$CACHE_DIR/.mypy_cache" .mypy_cache
ln -sf "$CACHE_DIR/.ruff_cache" .ruff_cache
ln -sf "$CACHE_DIR/htmlcov" htmlcov
ln -sf "$CACHE_DIR/.coverage" .coverage
ln -sf "$CACHE_DIR/coverage.xml" coverage.xml

# Exportar variáveis de ambiente
export PYTHONPATH="$PWD/src"
export PROJECT_NAME="py-ia-rom-logger"
export PYTHONPYCACHEPREFIX="$CACHE_DIR/pycache"
export RUFF_CACHE_DIR="$CACHE_DIR/.ruff_cache"
export MYPY_CACHE_DIR="$CACHE_DIR/.mypy_cache"
export PYTEST_CACHE_DIR="$CACHE_DIR/.pytest_cache"
export COVERAGE_FILE="$CACHE_DIR/.coverage"
export COVERAGE_HTML_DIR="$CACHE_DIR/htmlcov"
export COVERAGE_XML_FILE="$CACHE_DIR/coverage.xml"

# Carregar .env se existir
if [ -f "configs/.env" ]; then
    set -a
    source configs/.env
    set +a
fi

echo -e "${GREEN}✓ Ambiente ativado: py-ia-rom-logger${NC}"
echo -e "${GREEN}  Virtual env: $VENV_PATH${NC}"
echo -e "${GREEN}  Cache dir: $CACHE_DIR${NC}"
