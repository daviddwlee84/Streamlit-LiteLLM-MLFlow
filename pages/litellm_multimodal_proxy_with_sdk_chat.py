from uuid import uuid4
import streamlit as st
from litellm import completion, get_valid_models
from dotenv import load_dotenv, find_dotenv
import mlflow.litellm
import base64
from PIL import Image
import io
from streamlit.runtime.uploaded_file_manager import UploadedFile

load_dotenv(find_dotenv())
mlflow.litellm.autolog()

# https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps/build-conversational-apps

mlflow.set_experiment("LiteLLM Multimodal Chat Image (Proxy + SDK) with MLFlow autolog")

st.title(
    "ChatGPT-like clone (litellm Multimodal Chat Image (Proxy + SDK) with MLFlow autolog)"
)
st.caption("NOTE: Log to MLFlow with MLFlow autolog")

valid_models = get_valid_models(
    check_provider_endpoint=True, custom_llm_provider="litellm_proxy"
)


st.session_state["model"] = st.selectbox("Select Model", valid_models)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "session_id" not in st.session_state:
    st.session_state["session_id"] = str(uuid4())


def process_uploaded_image(uploaded_file: UploadedFile) -> str | None:
    """Process uploaded image and convert to base64 format for LiteLLM"""
    if uploaded_file is None:
        return None

    try:
        # Read the uploaded file as PIL Image
        image = Image.open(uploaded_file)

        # Get image format from file extension
        file_extension = uploaded_file.name.split(".")[-1].lower()
        if file_extension == "jpg":
            file_extension = "jpeg"

        # Convert image to RGB if it's not already
        if image.mode != "RGB":
            image = image.convert("RGB")

        # Convert image to base64
        buffer = io.BytesIO()
        image.save(buffer, format=file_extension.upper())
        encoded_image = base64.b64encode(buffer.getvalue()).decode("utf-8")

        return f"data:image/{file_extension};base64,{encoded_image}"

    except Exception as e:
        st.error(f"Failed to process the image: {str(e)}")
        return None


def clear_messages():
    st.session_state.messages.clear()
    st.session_state.session_id = str(uuid4())
    st.toast("Messages cleared.")


st.button("Clear Messages", on_click=clear_messages)

# 回放歷史訊息
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if isinstance(message["content"], list):
            # Handle multimodal content (text + image)
            for item in message["content"]:
                if item["type"] == "text":
                    st.markdown(item["text"])
                elif item["type"] == "image_url":
                    st.image(
                        item["image_url"]["url"], caption="Uploaded Image", width=200
                    )
        else:
            # Handle text-only content
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
if prompt := st.chat_input(
    "What is up?", accept_file=True, file_type=["png", "jpg", "jpeg", "gif", "webp"]
):

    # Process uploaded image if any
    image_url = (
        process_uploaded_image(prompt["files"][0])
        if "files" in prompt and len(prompt["files"]) > 0
        else None
    )

    # Create message content based on whether there's an image
    if image_url:
        # Multimodal message with text and image
        message_content = [
            {"type": "text", "text": prompt.text},
            {"type": "image_url", "image_url": {"url": image_url}},
        ]
        st.session_state.messages.append({"role": "user", "content": message_content})

        # Display user message with image
        with st.chat_message("user"):
            st.markdown(prompt.text)
            st.image(image_url, caption="Uploaded Image", width=200)
    else:
        # Text-only message
        st.session_state.messages.append({"role": "user", "content": prompt.text})
        with st.chat_message("user"):
            st.markdown(prompt.text)

    with st.chat_message("assistant"):
        # Process messages for completion call - handle multimodal content
        processed_messages = []
        for m in st.session_state.messages:
            if isinstance(m["content"], list):
                # Multimodal message - keep as is
                processed_messages.append({"role": m["role"], "content": m["content"]})
            else:
                # Text-only message
                processed_messages.append({"role": m["role"], "content": m["content"]})

        response = st.write_stream(
            stream_litellm(
                messages=processed_messages,
                model=st.session_state["model"],
                user_id=st.session_state.get("username")
                or st.session_state.get("email")
                or "anonymous",
                session_id=st.session_state["session_id"],
            )
        )
    st.session_state.messages.append({"role": "assistant", "content": response})
