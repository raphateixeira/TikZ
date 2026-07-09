#!/usr/bin/env bash
# Recompila as figuras pendentes, regenera as páginas da galeria e renderiza
# o site Quarto. Rode a partir de qualquer diretório.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

python3 scripts/build_figuras.py "$@"
python3 scripts/generate_gallery.py
quarto render
