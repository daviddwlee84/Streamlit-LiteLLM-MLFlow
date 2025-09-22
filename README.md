# Streamlit x LiteLLM x MLFlow

LiteLLM as LLM Proxy, MLFlow for LLM Tracing and Prompt Management

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

## Todo

- [ ] Prompt (MLFlow)
- [x] LiteLLM Proxy
- [x] Docker Compose (LiteLLM Proxy + Streamlit + MLFlow)
- [ ] Load history messages from MLFlow
