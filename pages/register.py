"""
Registration page for new users.
"""

import streamlit as st

from streamlit_litellm_mlflow import render_register_form


def main():
    """Registration page."""
    st.title("📝 Create Account")

    st.info("Welcome! Please create your account to get started.")

    render_register_form()

    st.markdown("---")
    col1, col2 = st.columns([1, 1])
    with col1:
        if st.button("← Back to Login", use_container_width=True):
            st.switch_page("pages/login.py")


if __name__ == "__main__":
    main()
