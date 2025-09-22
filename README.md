# Streamlit x LiteLLM x MLFlow

LiteLLM as LLM Proxy, MLFlow for LLM Tracing and Prompt Management

```bash
uv sync --all-groups
uv run streamlit run main.py
uv run mlflow ui --backend-store-uri sqlite:///mlflow.db
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

---

## Trouble Shooting

Claude can't be use in HK

```
litellm.exceptions.BadRequestError: litellm.BadRequestError: BedrockException - {"message":"Access to Anthropic models is not allowed from unsupported countries, regions, or territories. Please refer to https://www.anthropic.com/supported-countries for more information on the countries and regions Anthropic currently supports."}. Received Model Group=bedrock-claude-3-7
```

Seems litellm not loading MLFLOW_TRACKING_URI from .env (not sure if this will conflict, need test)

```
2025/09/22 11:21:45 WARNING mlflow.tracing.export.mlflow_v3: Failed to send trace to MLflow backend: When an mlflow-artifacts URI was supplied, the tracking URI must be a valid http or https URI, but it was currently set to sqlite:/mlflow.db. Perhaps you forgot to set the tracking URI to the running MLflow server. To set the tracking URI, use either of the following methods:
1. Set the MLFLOW_TRACKING_URI environment variable to the desired tracking URI. `export MLFLOW_TRACKING_URI=http://localhost:5000`
2. Set the tracking URI programmatically by calling `mlflow.set_tracking_uri`. `mlflow.set_tracking_uri('http://localhost:5000')`
```
