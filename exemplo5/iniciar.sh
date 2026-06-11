#!/bin/zsh

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
VENV_PYTHON="$PROJECT_DIR/.venv/bin/python"
APP_FILE="$SCRIPT_DIR/exemplo5-v1.py"
FRONT_URL="http://127.0.0.1:5000/"

if [ -x "$VENV_PYTHON" ]; then
    PYTHON_CMD="$VENV_PYTHON"
else
    PYTHON_CMD="python3"
fi

echo "Iniciando front e back do exemplo5..."
echo "Front disponivel em: $FRONT_URL"
echo "Pressione Ctrl+C para encerrar."

cd "$SCRIPT_DIR"
exec "$PYTHON_CMD" "$APP_FILE"
