from uuid import uuid4
import streamlit as st
from litellm import completion, get_valid_models
from dotenv import load_dotenv, find_dotenv
import mlflow.litellm

load_dotenv(find_dotenv())
mlflow.litellm.autolog()

# https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/build-conversational-apps

mlflow.set_experiment("LiteLLM Proxy with SDK")

st.title("ChatGPT-like clone (litellm Proxy with SDK)")
st.caption("NOTE: we try to log to MLFlow using LiteLLM Proxy Callback")

with st.expander("User Info"):
    st.write(st.session_state.get("authentication_status"))
    st.write(st.session_state.get("username"))
    st.write(st.session_state.get("name"))
    st.write(st.session_state.get("email"))

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


def stream_litellm(
    messages: list[dict],
    model: str,
    user_id: str,
    session_id: str,
):
    # https://docs.litellm.ai/docs/proxy/logging#mlflow
    # https://docs.litellm.ai/docs/observability/mlflow#adding-tags-for-better-tracing

    # litellm 的 streaming 會 yield OpenAI 風格的 chunk
    resp = completion(
        model=model,
        messages=messages,
        stream=True,
        # BUG: this will only record to request_tags instead of trace_tags
        metadata={
            "tags": [
                f"mlflow.trace.user:{user_id}",
                f"mlflow.trace.session:{session_id}",
            ]
        },
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
    # ValueError: Model is None and does not exist in passed completion_response. Passed completion_response=<litellm.litellm_core_utils.streaming_handler.CustomStreamWrapper object at 0x1438337d0>, model=None
    # Exception: This model isn't mapped yet. model=litellm_proxy/bedrock-claude-3-7, custom_llm_provider=litellm_proxy. Add it here - https://github.com/BerriAI/litellm/blob/main/model_prices_and_context_window.json.
    # st.toast(f"Response cost (full): {completion_cost(resp, model=model, prompt=full)}")
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
