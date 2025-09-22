#!/bin/bash

# Streamlit-LiteLLM-MLFlow 啟動腳本

echo "🚀 啟動 Streamlit-LiteLLM-MLFlow 應用..."

# 檢查 .env 文件是否存在
if [ ! -f .env ]; then
    echo "⚠️  .env 文件不存在，正在從 environment.example 創建..."
    cp environment.example .env
    echo "✅ 已創建 .env 文件，請編輯它並填入您的 API 金鑰"
    echo "📝 編輯完成後重新運行此腳本"
    exit 1
fi

# 檢查必要的環境變數
missing_vars=()
for var in AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY OPENAI_API_KEY; do
    if [ -z "${!var}" ]; then
        missing_vars+=("$var")
    fi
done

if [ ${#missing_vars[@]} -ne 0 ]; then
    echo "❌ 缺少必要的環境變數: ${missing_vars[*]}"
    echo "📝 請在 .env 文件中設置這些變數"
    exit 1
fi

echo "✅ 環境檢查完成"

# 確保數據庫文件存在
if [ ! -f users.db ]; then
    echo "📄 創建用戶數據庫..."
    touch users.db
fi

if [ ! -f mlflow.db ]; then
    echo "📄 創建 MLFlow 數據庫..."
    touch mlflow.db
fi

# 啟動 Docker Compose
echo "🐳 啟動 Docker 服務..."
docker-compose up --build

echo "🎉 所有服務已啟動！"
echo "📱 Streamlit: http://localhost:8501"
echo "🔗 LiteLLM: http://localhost:4000"
echo "📊 MLFlow: http://localhost:5000"
echo ""
echo "按 Ctrl+C 停止所有服務"
