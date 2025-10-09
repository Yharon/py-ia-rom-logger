#!/bin/bash
# activate_env.sh - Environment activation for py-ia-rom-logger
#
# ⚠️ NOTE: This project uses direnv for automatic environment management!
#
# RECOMMENDED USAGE:
#   Just cd into the project directory - direnv will handle everything:
#   $ cd /path/to/py-ia-rom-logger
#
# If direnv is not installed or you need manual activation:
#   $ source activate_env.sh
#
# What this script does (automatically via direnv):
#   - Activates Python virtual environment
#   - Creates external cache symlinks
#   - Exports environment variables
#   - Loads project .env file

# Check if direnv is active
if [ -n "$DIRENV_DIR" ]; then
    echo "✓ direnv is already active - environment loaded automatically"
    return 0
fi

# Fallback: Manual activation (if direnv not available)
echo "⚠️  direnv not detected - activating manually..."

# Verificar se RES_ENVS e RES_ROOT estão definidos
if [ -z "$RES_ENVS" ] || [ -z "$RES_ROOT" ]; then
    echo "❌ Variáveis RES_ENVS ou RES_ROOT não definidas"
    echo "Defina-as no seu ~/.bashrc ou ~/.zshrc"
    return 1
fi

# Source the .envrc file (which contains all the logic)
if [ -f ".envrc" ]; then
    # direnv's eval equivalent
    source ".envrc"
else
    echo "❌ .envrc not found - cannot activate environment"
    return 1
fi
