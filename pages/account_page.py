import streamlit as st

from streamlit_litellm_mlflow import (
    build_authenticator,
    init_db,
    load_credentials,
    render_change_password_form,
)


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
            st.switch_page("pages/welcome_page.py")

    st.markdown("---")
    st.subheader("Change Password")
    render_change_password_form(st.session_state.get("username"))


if __name__ == "__main__":
    account_page()
