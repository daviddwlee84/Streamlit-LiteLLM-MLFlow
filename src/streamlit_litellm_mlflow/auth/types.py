"""
Type definitions for authentication module.
"""

from typing import Dict, TypedDict


class UserRow(TypedDict):
    """Database user row structure."""

    user_id: int
    username: str
    name: str
    email: str
    password: str  # bcrypt hash
    role: str


Credentials = Dict[
    str, Dict[str, Dict[str, str]]
]  # {"usernames": {uname: {"name":..., "email":..., "password":...}}}
