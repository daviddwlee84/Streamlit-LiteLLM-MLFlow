import streamlit as st


st.set_page_config(page_title="Streamlit-LiteLLM-MLFlow", page_icon="🚀", layout="wide")

# Build navigation dynamically based on authentication status
is_authenticated = st.session_state.get("authentication_status")

if is_authenticated:
    pages = {
        "Application": [
            st.Page(
                "pages/1_Simplest_Chat.py",
                url_path="simplest_chat",
                title="Simple Chat",
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
