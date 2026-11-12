#!/bin/bash
set -euo pipefail

HF_BIN="/lhome/ific/d/dancon/.conda/envs/grant-extract/bin/hf"
MODEL_DIR="/lhome/ific/d/dancon/LLModels/Qwen2.5-7B-Instruct"

if [ ! -x "$HF_BIN" ]; then
    echo "ERROR: hf not found at $HF_BIN" >&2
    exit 1
fi

mkdir -p "$MODEL_DIR"
echo "Downloading Qwen/Qwen2.5-7B-Instruct to $MODEL_DIR ..."

"$HF_BIN" download Qwen/Qwen2.5-7B-Instruct --local-dir "$MODEL_DIR"

echo "Done. Contents:"
ls -lh "$MODEL_DIR"