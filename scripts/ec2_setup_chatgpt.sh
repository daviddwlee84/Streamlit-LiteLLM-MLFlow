#!/usr/bin/env bash
# NOTE: this basically works
# Bootstrap an Ubuntu EC2 for uv-based Python projects (cp312) + native builds
# tested on Ubuntu 22.04/24.04 (x86_64)

set -euo pipefail
export DEBIAN_FRONTEND=noninteractive

# --- System deps for building native/python wheels ---
sudo apt-get update
sudo apt-get install -y --no-install-recommends \
  build-essential gcc g++ make \
  pkg-config cmake ninja-build \
  curl ca-certificates git \
  sqlite3 \
  libssl-dev libffi-dev \
  libsqlite3-dev zlib1g-dev \
  libbz2-dev liblzma-dev \
  libreadline-dev libncursesw5-dev

# Python headers (try generic and versioned, tolerate misses)
sudo apt-get install -y python3-dev python3-venv || true
sudo apt-get install -y python3.12-dev || true   # 24.04 常見
sudo apt-get install -y python3.10-dev || true   # 22.04 常見

# --- uv (Python 包管理/虛擬環境) ---
# https://docs.astral.sh/uv/getting-started/installation/
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"

# --- Rust toolchain (部分輪子沒有預編譯時會 fallback 到 cargo build) ---
# https://www.rust-lang.org/tools/install
if ! command -v rustc >/dev/null 2>&1; then
  curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
fi
# shellcheck disable=SC1091
source "$HOME/.cargo/env"

# --- Ensure a CPython 3.12 is available for the project ---
uv python install 3.12

# （可選）若你要專案獨立 venv，建議建一個 .venv
uv venv .venv --python 3.12
# shellcheck disable=SC1091
source .venv/bin/activate

# --- Sync project deps ---
# 若你在 pyproject.toml 內用了鏡像（如 TUNA），uv 會遵循該設定。
# 鏡像缺輪子時可能觸發 from-source 編譯；有了上方 dev headers 就能過。
uv sync --all-groups

# --- Quick smoke test ---
python - <<'PY'
import sys
print("Python:", sys.version)
import litellm, mlflow, pandas
print("litellm:", getattr(litellm, "__version__", "?"))
print("mlflow:", getattr(__import__("mlflow"), "__version__", "?"))
print("pandas:", __import__("pandas").__version__)
PY

echo "✅ Setup finished."