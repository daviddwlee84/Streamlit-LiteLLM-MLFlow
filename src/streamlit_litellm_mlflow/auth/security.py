"""
Security utilities for password hashing and verification.
"""

import bcrypt


def bcrypt_hash_password(plain_password: str) -> str:
    """Hash password with bcrypt (utf-8)."""
    if not plain_password:
        raise ValueError("Empty password")
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(plain_password.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def bcrypt_verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify bcrypt password."""
    if not plain_password or not hashed_password:
        return False
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )
    except Exception:
        return False
