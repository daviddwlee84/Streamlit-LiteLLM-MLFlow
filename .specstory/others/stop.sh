#!/bin/bash

# Streamlit-LiteLLM-MLFlow 停止腳本

echo "🛑 停止 Streamlit-LiteLLM-MLFlow 應用..."

# 停止 Docker Compose 服務
echo "🐳 停止 Docker 服務..."
docker-compose down

echo "✅ 所有服務已停止！"
