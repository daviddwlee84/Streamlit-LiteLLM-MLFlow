# 使用官方 Python 3.12 作為基礎映像
FROM python:3.12-slim

# 設定工作目錄
WORKDIR /app

# 安裝系統依賴
RUN apt-get update && apt-get install -y \
    sqlite3 \
    build-essential \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 安裝 Rust（因為某些 Python 包如 fastuuid 需要 Rust）
RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh -s -- -y
ENV PATH="/root/.cargo/bin:${PATH}"

# 複製依賴文件
COPY requirements.txt .
COPY pyproject.toml .
COPY uv.lock .

# 安裝 Python 依賴
RUN pip install --no-cache-dir -r requirements.txt -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple

# 複製應用程式代碼
COPY main.py .
COPY src/ ./src/
COPY .streamlit/ ./.streamlit/

# 創建非 root 用戶
RUN useradd --create-home --shell /bin/bash streamlit
RUN chown -R streamlit:streamlit /app
USER streamlit

# 暴露 Streamlit 預設埠
EXPOSE 8501

# 健康檢查
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8501/_stcore/health || exit 1

# 啟動 Streamlit 應用程式
CMD ["streamlit", "run", "main.py", "--server.port", "8501", "--server.address", "0.0.0.0"]
