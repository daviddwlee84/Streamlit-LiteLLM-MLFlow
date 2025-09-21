import streamlit as st

from streamlit_litellm_mlflow import (
    build_authenticator,
    init_db,
    load_credentials,
    render_change_password_form,
    render_register_form,
)


def login_page():
    """Login page that shows when user is not authenticated."""
    st.title("🔐 Login Required")

    # Initialize database and load credentials
    init_db()
    creds = load_credentials()

    # Check if there are any registered users
    has_users = len(creds["usernames"]) > 0

    if has_users:
        # Only show login form if there are users
        authenticator = build_authenticator(creds)
        authenticator.login(location="main", key="Login")

        # Handle authentication status
        if st.session_state.get("authentication_status"):
            st.success(
                f"Welcome, {st.session_state.get('name')} (@{st.session_state.get('username')})"
            )
            st.info("Please use the navigation menu to access application pages.")
            authenticator.logout(
                button_name="Logout", location="sidebar", key="Logout_main"
            )
        elif st.session_state.get("authentication_status") is False:
            st.error("Invalid username or password.")
            st.info("If you don't have an account, register below.")
            render_register_form()
        else:
            st.info("Please enter your username and password.")
            render_register_form()
    else:
        # No users registered yet - only show registration
        st.info("No users registered yet. Please create your first account below.")
        render_register_form()

    # Sidebar for logged-in users
    with st.sidebar:
        st.markdown("### Account")
        if has_users and st.session_state.get("authentication_status"):
            st.success(f"✅ Logged in as **{st.session_state.get('username')}**")
            authenticator.logout("Logout", key="Logout_sidebar")
        else:
            st.info("Not logged in")

        st.markdown("---")
        st.caption("Password hashes are stored with bcrypt in users.db / sa_users.")


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
            authenticator.logout()
            st.rerun()

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
        # Show login page if not authenticated
        login_page()
        return

    # User is authenticated - show main application pages
    pages = {
        "Chat": [
            st.Page("auth_pages/1_Simplest_Chat.py", title="Simple Chat", icon="💬"),
        ],
        "Account": [
            st.Page(account_page, title="Account Settings", icon="⚙️"),
        ],
    }

    pg = st.navigation(pages, position="top")
    pg.run()


# TODO: register should redirect to login page
# TODO: logout should redirect to login page
# TODO: change password should redirect to login page
# TODO: logout should redirect to main page

if __name__ == "__main__":
    main()
