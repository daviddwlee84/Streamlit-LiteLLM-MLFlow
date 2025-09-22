import streamlit as st


st.set_page_config(page_title="Streamlit-LiteLLM-MLFlow", page_icon="🚀", layout="wide")

# Build navigation dynamically based on authentication status
is_authenticated = st.session_state.get("authentication_status")

if is_authenticated:
    pages = {
        "Application": [
            st.Page(
                "pages/litellm_sdk.py",
                url_path="litellm_sdk",
                title="LiteLLM SDK",
                icon="💬",
            ),
            st.Page(
                "pages/litellm_sdk_with_user_info.py",
                url_path="litellm_sdk_with_user_info",
                title="LiteLLM SDK with User Info",
                icon="💬",
            ),
            st.Page(
                "pages/litellm_proxy_with_sdk.py",
                url_path="litellm_proxy_with_sdk",
                title="LiteLLM Proxy with SDK",
                icon="💬",
            ),
            st.Page(
                "pages/litellm_multimodal_proxy_with_sdk.py",
                url_path="litellm_multimodal_proxy_with_sdk",
                title="LiteLLM Multimodal (Proxy + SDK) with MLFlow autolog",
                icon="💬",
            ),
        ],
        "Account": [
            st.Page(
                "pages/account_page.py",
                url_path="account_page",
                title="Account Settings",
                icon="⚙️",
            ),
        ],
    }
else:
    pages = {
        "Auth": [
            st.Page("pages/welcome_page.py", title="Welcome", icon="👋"),
            st.Page("pages/login.py", title="Login", icon="🔑"),
            st.Page("pages/register.py", title="Register", icon="📝"),
        ]
    }

pg = st.navigation(pages, position="top")
pg.run()
