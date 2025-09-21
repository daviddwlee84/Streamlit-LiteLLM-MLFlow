# Streamlit x LiteLLM x MLFlow

LiteLLM as LLM Proxy, MLFlow for LLM Tracing and Prompt Management

```bash
uv sync --all-groups
uv run streamlit run main.py
mlflow ui --backend-store-uri sqlite:///mlflow.db
```

## Todo

- [ ] Prompt (MLFlow)
- [ ] LiteLLM Proxy
- [ ] Docker Compose (LiteLLM Proxy + Streamlit + MLFlow)
