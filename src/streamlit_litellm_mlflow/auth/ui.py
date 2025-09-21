"""
UI components for authentication forms.
"""

import streamlit as st

from .database import (
    get_user_password_hash,
    insert_user,
    update_user_password,
    username_exists,
)
from .security import bcrypt_hash_password, bcrypt_verify_password


def render_register_form() -> None:
    """Render user registration form."""
    st.subheader("註冊 / Register")
    with st.form("register_form", clear_on_submit=False):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full name", key="reg_name")
            username = st.text_input(
                "Username", key="reg_username", autocomplete="username"
            )
            role = st.selectbox("Role", ["user", "admin"], index=0)
        with col2:
            email = st.text_input("Email", key="reg_email")
            password = st.text_input(
                "Password",
                type="password",
                key="reg_password",
                autocomplete="new-password",
            )
            password2 = st.text_input(
                "Confirm password",
                type="password",
                key="reg_password2",
                autocomplete="new-password",
            )

        submitted = st.form_submit_button("Create account")
    if submitted:
        if not (name and username and email and password):
            st.error("All fields are required.")
            return
        if password != password2:
            st.error("Passwords do not match.")
            return
        if username_exists(username):
            st.error("Username already exists.")
            return
        # hash & insert
        hashed = bcrypt_hash_password(password)
        insert_user(
            username=username, name=name, email=email, hashed_password=hashed, role=role
        )
        st.success(f"User **{username}** created successfully!")
        st.info("Redirecting to login page...")
        # Add a small delay and redirect
        st.balloons()
        if st.button("Continue to Login →", type="primary"):
            st.switch_page("pages/login.py")


def render_change_password_form(current_username: str) -> None:
    """Render password change form."""
    st.subheader("變更密碼 / Change Password")
    with st.form("change_pw_form", clear_on_submit=True):
        old_pw = st.text_input(
            "Current password", type="password", autocomplete="current-password"
        )
        new_pw = st.text_input(
            "New password", type="password", autocomplete="new-password"
        )
        new_pw2 = st.text_input(
            "Confirm new password", type="password", autocomplete="new-password"
        )
        submitted = st.form_submit_button("Change password")
    if submitted:
        if not (old_pw and new_pw):
            st.error("Please fill all password fields.")
            return
        if new_pw != new_pw2:
            st.error("New passwords do not match.")
            return
        stored_hash = get_user_password_hash(current_username)
        if not stored_hash or not bcrypt_verify_password(old_pw, stored_hash):
            st.error("Current password is incorrect.")
            return
        new_hash = bcrypt_hash_password(new_pw)
        update_user_password(current_username, new_hash)
        st.success("Password updated successfully!")
        st.info("Please login again with your new password.")
        # Clear session and redirect to login
        for key in ["authentication_status", "username", "name", "email"]:
            if key in st.session_state:
                del st.session_state[key]
        if st.button("Login with New Password →", type="primary"):
            st.switch_page("pages/login.py")
