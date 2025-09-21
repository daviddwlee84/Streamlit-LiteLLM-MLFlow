import streamlit as st
from litellm import completion
from dotenv import load_dotenv, find_dotenv
import mlflow.litellm

load_dotenv(find_dotenv())
mlflow.litellm.autolog()

# https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/build-conversational-apps

# TODO: record user info to mlflow

st.title("ChatGPT-like clone (litellm SDK)")

if "model" not in st.session_state:
    st.session_state["model"] = st.secrets.get("LITELLM_MODEL", "openai/gpt-4o-mini")

if "messages" not in st.session_state:
    st.session_state.messages = []

# 回放歷史訊息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


def stream_litellm(messages: list[dict], model: str):
    # litellm 的 streaming 會 yield OpenAI 風格的 chunk
    resp = completion(model=model, messages=messages, stream=True)
    full = ""
    for chunk in resp:
        delta = ""
        try:
            delta = chunk.choices[0].delta.get("content", "")  # OpenAI 風格
        except Exception:
            # 某些供應商回傳字段不同，做個保底
            delta = getattr(chunk, "content", "") or ""
        if delta:
            full += delta
            yield delta
    return full  # 讓 st.write_stream 拿到完整字串


# 輸入與串流輸出
if prompt := st.chat_input("What is up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = st.write_stream(
            stream_litellm(
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                model=st.session_state["model"],
            )
        )
    st.session_state.messages.append({"role": "assistant", "content": response})
