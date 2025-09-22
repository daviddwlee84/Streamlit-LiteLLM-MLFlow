import streamlit as st
from litellm import completion, completion_cost
from dotenv import load_dotenv, find_dotenv
import mlflow.litellm
import mlflow
from uuid import uuid4

load_dotenv(find_dotenv())
mlflow.litellm.autolog()

# https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/build-conversational-apps

mlflow.set_experiment("LiteLLM SDK with User Info")

st.title("ChatGPT-like clone (litellm SDK)")
st.caption("NOTE: we try log user and session info to MLFlow")
with st.expander("User Info"):
    st.write(st.session_state.get("authentication_status"))
    st.write(st.session_state.get("username"))
    st.write(st.session_state.get("name"))
    st.write(st.session_state.get("email"))

if "model" not in st.session_state:
    st.session_state["model"] = st.secrets.get("LITELLM_MODEL", "openai/gpt-4o-mini")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid4())


def clear_messages():
    st.session_state.messages.clear()
    st.session_state.session_id = str(uuid4())
    st.toast("Messages cleared. New session started.")


st.button("Clear Messages", on_click=clear_messages)

# 回放歷史訊息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


# https://mlflow.org/docs/latest/genai/tracing/track-users-sessions/
# https://mlflow.org/docs/latest/genai/tracing/lightweight-sdk/
# https://mlflow.org/docs/latest/genai/tracing/prod-tracing/
@mlflow.trace(name="litellm_sdk_with_user_info")
def stream_litellm(messages: list[dict], model: str, user_id: str, session_id: str):
    # litellm 的 streaming 會 yield OpenAI 風格的 chunk
    # Add user and session context to the current trace
    mlflow.update_current_trace(
        tags={
            "username": st.session_state.get("username"),
            "email": st.session_state.get("email"),
        },
        metadata={
            "mlflow.trace.user": user_id,  # Links trace to specific user
            "mlflow.trace.session": session_id,  # Groups trace with conversation
        },
    )

    # Your chat logic here
    resp = completion(model=model, messages=messages, stream=True)

    # 把使用者資訊打到 MLflow 當前的 tracing run 上
    # try:
    #     mlflow.set_tag("user_id", user_id)
    #     mlflow.set_tag("username", username or "")
    #     mlflow.set_tag("email", email or "")
    #     mlflow.set_tag("authentication_status", str(auth_status))
    #     mlflow.set_tag("session_id", session_id or "")
    #     mlflow.set_tag("client_request_id", client_request_id)
    # except Exception:
    #     # 避免因為 MLflow 標籤寫入失敗而影響聊天流程
    #     pass
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

    # TODO: tracing cost to MLFlow
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
                user_id=st.session_state.get("username")
                or st.session_state.get("email")
                or "anonymous",
                session_id=st.session_state["session_id"],
            )
        )
    st.session_state.messages.append({"role": "assistant", "content": response})
