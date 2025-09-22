#!/usr/bin/env bash
# NOTE: haven't tested yet
# start-tmux.sh - One-click tmux launcher for Streamlit + MLflow UI + LiteLLM
set -euo pipefail

# === Config ===
PROJECT_DIR="${PROJECT_DIR:-$(pwd)}"
SESSION_NAME="${SESSION_NAME:-sllm}"   # 你可以 export SESSION_NAME=myproj 覆蓋
# 可選：附加參數（例如 EC2 想對外開放就加 --server.address=0.0.0.0）
STREAMLIT_ARGS="${STREAMLIT_ARGS:-}"
MLFLOW_ARGS="${MLFLOW_ARGS:-}"
LITELLM_ARGS="${LITELLM_ARGS:-}"

# === Ensure tmux ===
if ! command -v tmux >/dev/null 2>&1; then
  echo "[i] tmux 未安裝，嘗試使用 apt 裝上..."
  if command -v apt-get >/dev/null 2>&1; then
    sudo apt-get update
    sudo apt-get install -y tmux
  else
    echo "[!] 找不到 apt，請手動安裝 tmux 後重試"; exit 1
  fi
fi

# === Load .env (if present) ===
if [ -f "$PROJECT_DIR/.env" ]; then
  echo "[i] 載入 .env ..."
  set -a
  # shellcheck disable=SC1090
  source "$PROJECT_DIR/.env"
  set +a
fi

# === uv in PATH (若用官方安裝器，通常在 ~/.local/bin) ===
export PATH="$HOME/.local/bin:$PATH"

# === Recreate session ===
if tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
  echo "[i] 已存在 tmux session '$SESSION_NAME'，先刪除再重建"
  tmux kill-session -t "$SESSION_NAME"
fi

# === Window 1: Streamlit app ===
tmux new-session -d -s "$SESSION_NAME" -c "$PROJECT_DIR" -n "app"
tmux set-option -t "$SESSION_NAME" allow-rename off
tmux send-keys -t "$SESSION_NAME:app" "uv run streamlit run main.py $STREAMLIT_ARGS" C-m

# === Window 2: MLflow UI ===
tmux new-window -t "$SESSION_NAME" -n "mlflow" -c "$PROJECT_DIR"
tmux send-keys -t "$SESSION_NAME:mlflow" "uv run mlflow ui --backend-store-uri sqlite:///mlflow.db $MLFLOW_ARGS" C-m

# === Window 3: LiteLLM Proxy ===
tmux new-window -t "$SESSION_NAME" -n "litellm" -c "$PROJECT_DIR"
tmux send-keys -t "$SESSION_NAME:litellm" "uv run litellm --config ./litellm_config.yaml $LITELLM_ARGS" C-m

# 聚焦第一個視窗並附著
tmux select-window -t "$SESSION_NAME:app"
tmux attach -t "$SESSION_NAME"
