import streamlit as st

from streamlit_litellm_mlflow import init_db, load_credentials


def welcome_page():
    """Welcome page that redirects to appropriate auth page."""
    st.title("🚀 Welcome to Streamlit-LiteLLM-MLFlow")

    # Initialize database and check if users exist
    init_db()
    creds = load_credentials()
    has_users = len(creds["usernames"]) > 0

    st.markdown(
        """
    ### 🤖 AI-Powered Chat Application

    This application provides:
    - 🔐 **Secure Authentication** - User management with password protection
    - 💬 **Chat Interface** - Simple and intuitive chat experience
    - 🚀 **LiteLLM Integration** - AI model proxy capabilities
    - 📊 **MLFlow Tracking** - Experiment and prompt management
    """
    )

    st.markdown("---")

    if has_users:
        st.subheader("🔐 Access Your Account")
        col1, col2 = st.columns([1, 1])

        with col1:
            if st.button("🔑 Login", type="primary", use_container_width=True):
                st.switch_page("pages/login.py")

        with col2:
            if st.button("📝 Create Account", use_container_width=True):
                st.switch_page("pages/register.py")
    else:
        st.subheader("🎉 Get Started")
        st.info("No users registered yet. Create your first account to begin!")

        if st.button(
            "📝 Create First Account", type="primary", use_container_width=True
        ):
            st.switch_page("pages/register.py")


if __name__ == "__main__":
    welcome_page()
