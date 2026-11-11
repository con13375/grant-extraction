#!/bin/bash
# download_qwen.sh
# Descarga Qwen 2.5 7B Instruct en un nodo de cómputo de Artemisa.

set -euo pipefail

# Ruta donde guardar el modelo. Cámbiala si prefieres otro sitio.
MODEL_DIR="$HOME/models/Qwen2.5-7B-Instruct"

mkdir -p "$MODEL_DIR"

echo "Descargando Qwen/Qwen2.5-7B-Instruct en $MODEL_DIR ..."

# El comando puede ser 'hf download' o 'huggingface-cli download' según la versión
hf download Qwen/Qwen2.5-7B-Instruct \
    --local-dir "$MODEL_DIR" \
    --local-dir-use-symlinks False

echo "Descarga completada. Contenido:"
ls -lh "$MODEL_DIR"
