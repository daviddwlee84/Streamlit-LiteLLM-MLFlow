"""
Login page for existing users.
"""

import streamlit as st

from streamlit_litellm_mlflow import (
    build_authenticator,
    init_db,
    load_credentials,
)


def main():
    """Login page."""
    st.title("🔐 Login")

    # Initialize database and load credentials
    init_db()
    creds = load_credentials()

    # Check if there are any registered users
    has_users = len(creds["usernames"]) > 0

    if not has_users:
        st.warning("No users registered yet. Please create an account first.")
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Create Account →", type="primary", use_container_width=True):
                st.switch_page("pages/register.py")
        return

    # Show login form
    authenticator = build_authenticator(creds)
    authenticator.login(location="main", key="Login")

    # Handle authentication status
    if st.session_state.get("authentication_status"):
        st.success(f"Welcome back, {st.session_state.get('name')}!")
        st.info("Redirecting to application...")
        # Redirect to main page after successful login
        st.switch_page("main.py")
    elif st.session_state.get("authentication_status") is False:
        st.error("Invalid username or password.")
    else:
        st.info("Please enter your credentials to continue.")

    # Navigation to register page
    st.markdown("---")
    col1, col2 = st.columns([1, 1])
    with col2:
        if st.button("Create Account →", use_container_width=True):
            st.switch_page("pages/register.py")


main()
