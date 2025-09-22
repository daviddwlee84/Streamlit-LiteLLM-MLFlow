
## 🚀 快速開始 (Docker Compose)

### 一鍵啟動所有服務

```bash
# 1. 克隆項目
git clone <your-repo-url>
cd Streamlit-LiteLLM-MLFlow

# 2. 設置環境變數
cp environment.example .env
# 編輯 .env 文件，填入您的 API 金鑰

# 3. 啟動所有服務
./start.sh

# 停止所有服務
./stop.sh
```

### 服務地址

啟動後您可以訪問：
- **Streamlit 應用**: http://localhost:8501
- **LiteLLM Proxy**: http://localhost:4000
- **MLFlow UI**: http://localhost:5000

### 手動啟動 (可選)

```bash
# 使用 Docker Compose
docker-compose up --build

# 或使用單個服務
docker-compose up streamlit
docker-compose up litellm
docker-compose up mlflow
```

## 📝 環境變數設置

複製 `environment.example` 為 `.env` 並填入以下變數：

```bash
# AWS Credentials for Bedrock
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_REGION_NAME=us-east-1

# OpenAI API Key
OPENAI_API_KEY=sk-your-openai-api-key

# Gemini API Key
GEMINI_API_KEY=your-gemini-api-key
```

## 🔧 開發環境設置

### 傳統方式 (不使用 Docker)

```bash
uv sync --all-groups
uv run streamlit run main.py
mlflow ui --backend-store-uri sqlite:///mlflow.db
```

```bash
uv run litellm --config ./litellm_config.yaml

# https://docs.litellm.ai/docs/proxy/docker_quick_start#22-make-call
curl -X POST 'http://localhost:4000/chat/completions' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer sk-1234' \
-d '{
    "model": "bedrock-nova-pro",
    "messages": [
      {
        "role": "system",
        "content": "You are an LLM named gpt-4o"
      },
      {
        "role": "user",
        "content": "what is your name?"
      }
    ],
    "litellm_metadata": {
      "tags": [
        "mlflow.trace.user:user_42",
        "mlflow.trace.session:sess_2025-09-22_A"
      ]
    }
}'

# https://docs.litellm.ai/docs/proxy/model_management#usage
curl -X GET "http://localhost:4000/model/info" \
    -H 'Content-Type: application/json' \
    -H 'Authorization: Bearer sk-1234'
```
