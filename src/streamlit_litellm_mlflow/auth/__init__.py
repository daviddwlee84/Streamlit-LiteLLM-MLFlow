"""
Authentication module for Streamlit applications with SQLite backend.
"""

from .authenticator import build_authenticator
from .database import init_db, load_credentials
from .ui import render_change_password_form, render_register_form

__all__ = [
    "build_authenticator",
    "init_db",
    "load_credentials",
    "render_change_password_form",
    "render_register_form",
]
