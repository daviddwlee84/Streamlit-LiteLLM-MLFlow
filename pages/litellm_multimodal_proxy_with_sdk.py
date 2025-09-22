from uuid import uuid4
import streamlit as st
from litellm import completion, get_valid_models
from dotenv import load_dotenv, find_dotenv
import mlflow.litellm

load_dotenv(find_dotenv())
mlflow.litellm.autolog()

# https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/build-conversational-apps

mlflow.set_experiment("LiteLLM Multimodal (Proxy + SDK) with MLFlow autolog")

st.title("ChatGPT-like clone (litellm Multimodal (Proxy + SDK) with MLFlow autolog)")
st.caption("NOTE: Log to MLFlow with MLFlow autolog")

valid_models = get_valid_models(
    check_provider_endpoint=True, custom_llm_provider="litellm_proxy"
)


st.session_state["model"] = st.selectbox("Select Model", valid_models)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid4())


def clear_messages():
    st.session_state.messages.clear()
    st.session_state.session_id = str(uuid4())
    st.toast("Messages cleared.")


st.button("Clear Messages", on_click=clear_messages)

# 回放歷史訊息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


@mlflow.trace
def stream_litellm(
    messages: list[dict],
    model: str,
    user_id: str,
    session_id: str,
):
    # https://docs.litellm.ai/docs/proxy/logging#mlflow
    # https://docs.litellm.ai/docs/observability/mlflow#adding-tags-for-better-tracing

    mlflow.update_current_trace(
        metadata={
            "mlflow.trace.user": user_id,  # Links trace to specific user
            "mlflow.trace.session": session_id,  # Groups trace with conversation
        },
    )

    # litellm 的 streaming 會 yield OpenAI 風格的 chunk
    resp = completion(
        model=model,
        messages=messages,
        stream=True,
    )

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
                user_id=st.session_state.get("username")
                or st.session_state.get("email")
                or "anonymous",
                session_id=st.session_state["session_id"],
            )
        )
    st.session_state.messages.append({"role": "assistant", "content": response})
