"""
Streamlit-authenticator integration.
"""

import os

import streamlit_authenticator as stauth

from .types import Credentials


def build_authenticator(creds: Credentials) -> stauth.Authenticate:
    """
    Create streamlit-authenticator instance with cookie config.
    NOTE: For production: put keys in secrets!
    """
    cookie_name = "sa_demo_app"
    # WARNING: demo purpose only. Use a fixed secret from st.secrets in real apps.
    signature_key = os.environ.get(
        "SA_COOKIE_KEY", "streamlit-auth-demo-key-2024-secure-random"
    )
    return stauth.Authenticate(
        credentials=creds,
        cookie_name=cookie_name,
        key=signature_key,
        cookie_expiry_days=7,
    )
