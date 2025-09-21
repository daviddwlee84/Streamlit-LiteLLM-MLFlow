import streamlit as st


st.set_page_config(page_title="Streamlit-LiteLLM-MLFlow", page_icon="🚀", layout="wide")

# Check authentication status
if not st.session_state.get("authentication_status"):
    # Redirect to welcome page if not authenticated
    st.switch_page("pages/welcome_page.py")

# User is authenticated - show main application pages
pages = {
    "Application": [
        st.Page("pages/1_Simplest_Chat.py", title="Simple Chat", icon="💬"),
    ],
    "Account": [
        st.Page("pages/account_page.py", title="Account Settings", icon="⚙️"),
    ],
}

pg = st.navigation(pages, position="top")
pg.run()
