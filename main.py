import streamlit as st

from streamlit_litellm_mlflow import (
    build_authenticator,
    init_db,
    load_credentials,
    render_change_password_form,
    render_register_form,
)


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


def account_page():
    """Account settings page for authenticated users."""
    st.title("⚙️ Account Settings")

    st.markdown(
        f"**Welcome, {st.session_state.get('name')}** (@{st.session_state.get('username')})"
    )

    # Initialize authenticator for logout
    init_db()
    creds = load_credentials()
    authenticator = build_authenticator(creds)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Account Information")
        st.write(f"**Username:** {st.session_state.get('username')}")
        st.write(f"**Name:** {st.session_state.get('name')}")
        st.write(f"**Email:** {st.session_state.get('email')}")

    with col2:
        st.subheader("Actions")
        if st.button("Logout", type="primary"):
            # Clear authentication status
            for key in ["authentication_status", "username", "name", "email"]:
                if key in st.session_state:
                    del st.session_state[key]

            # Use st.switch_page to redirect to main page
            # BUG: Could not find page: main.py
            st.switch_page("main.py")

    st.markdown("---")
    st.subheader("Change Password")
    render_change_password_form(st.session_state.get("username"))


def main():
    """Main application entry point with navigation."""
    st.set_page_config(
        page_title="Streamlit-LiteLLM-MLFlow", page_icon="🚀", layout="wide"
    )

    # Check authentication status
    if not st.session_state.get("authentication_status"):
        # Show welcome page if not authenticated
        welcome_page()
        return

    # User is authenticated - show main application pages
    pages = {
        "Application": [
            st.Page("pages/1_Simplest_Chat.py", title="Simple Chat", icon="💬"),
        ],
        "Account": [
            st.Page(account_page, title="Account Settings", icon="⚙️"),
        ],
    }

    pg = st.navigation(pages, position="top")
    pg.run()


if __name__ == "__main__":
    main()
