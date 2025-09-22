#!/bin/bash
# NOTE: not finished yet
# https://docs.astral.sh/uv/getting-started/installation/
curl -LsSf https://astral.sh/uv/install.sh | sh
sudo apt update && sudo apt install -y build-essential gcc g++ sqlite3 curl
source ~/.bashrc
# ```
#   × Failed to build `madoka==0.7.1`
#   ├─▶ The build backend returned an error
#   ╰─▶ Call to `setuptools.build_meta:__legacy__.build_wheel` failed (exit status: 1)
#
#       [stderr]
#       /home/ubuntu/.cache/uv/builds-v0/.tmpwftFyr/lib/python3.12/site-packages/setuptools/dist.py:759: SetuptoolsDeprecationWarning: License classifiers are deprecated.
#       !!
#
#               ********************************************************************************
#               Please consider removing the following classifiers in favor of a SPDX license expression:
#
#               License :: OSI Approved :: BSD License
#
#               See https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#license for details.
#               ********************************************************************************
#
#       !!
#         self._finalize_license_expression()
#       error: command 'x86_64-linux-gnu-g++' failed: No such file or directory
#
#       hint: This usually indicates a problem with the package or the build environment.
#   help: `madoka` (v0.7.1) was included because `streamlit-litellm-mlflow` (v0.1.0) depends on `litellm` (v1.77.3) which depends on `pondpond` (v1.4.1) which depends on `madoka`
# ```
# https://www.rust-lang.org/tools/install
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
uv sync --all-groups
source .venv/bin/activate


curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo sh -eux <<EOF
# Install newuidmap & newgidmap binaries
apt-get install -y uidmap
EOF
dockerd-rootless-setuptool.sh install
