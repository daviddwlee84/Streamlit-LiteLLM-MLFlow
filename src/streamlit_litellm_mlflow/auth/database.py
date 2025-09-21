"""
Database operations for authentication.
"""

import sqlite3
from typing import Final, List, Optional

from .types import Credentials, UserRow

# -------------------- Config --------------------
DB_PATH: Final[str] = "users.db"
TABLE: Final[str] = "sa_users"  # streamlit-authenticator 的 users 表
# TODO: make this configurable through environment variables


def get_conn(db_path: str = DB_PATH) -> sqlite3.Connection:
    """Open a SQLite connection with sane defaults."""
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db(db_path: str = DB_PATH, table: str = TABLE) -> None:
    """Create the auth table if it does not exist."""
    with get_conn(db_path) as conn:
        conn.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {table} (
                user_id     INTEGER PRIMARY KEY AUTOINCREMENT,
                username    TEXT UNIQUE NOT NULL,
                name        TEXT NOT NULL,
                email       TEXT NOT NULL,
                password    TEXT NOT NULL,       -- bcrypt hash
                role        TEXT NOT NULL DEFAULT 'user',
                created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        conn.commit()


def fetch_all_users(db_path: str = DB_PATH, table: str = TABLE) -> List[UserRow]:
    """Return all users as list of dict rows."""
    with get_conn(db_path) as conn:
        cur = conn.execute(
            f"SELECT user_id, username, name, email, password, role FROM {table};"
        )
        rows = [UserRow(**dict(r)) for r in cur.fetchall()]
    return rows


def load_credentials(db_path: str = DB_PATH, table: str = TABLE) -> Credentials:
    """
    Build `streamlit-authenticator` credentials dict from DB records.

    Returns:
        {"usernames": {username: {"name": name, "email": email, "password": bcrypt_hash}}}
    """
    creds: Credentials = {"usernames": {}}
    for r in fetch_all_users(db_path, table):
        creds["usernames"][r["username"]] = {
            "name": r["name"],
            "email": r["email"],
            "password": r["password"],  # already hashed
        }
    return creds


def username_exists(username: str, db_path: str = DB_PATH, table: str = TABLE) -> bool:
    """Check if username already exists."""
    with get_conn(db_path) as conn:
        cur = conn.execute(f"SELECT 1 FROM {table} WHERE username = ?;", (username,))
        return cur.fetchone() is not None


def insert_user(
    *,
    username: str,
    name: str,
    email: str,
    hashed_password: str,
    role: str = "user",
    db_path: str = DB_PATH,
    table: str = TABLE,
) -> None:
    """Insert a new user into the database."""
    with get_conn(db_path) as conn:
        conn.execute(
            f"INSERT INTO {table} (username, name, email, password, role) VALUES (?, ?, ?, ?, ?);",
            (username, name, email, hashed_password, role),
        )
        conn.commit()


def update_user_password(
    username: str, new_hashed_password: str, db_path: str = DB_PATH, table: str = TABLE
) -> None:
    """Update user password."""
    with get_conn(db_path) as conn:
        cur = conn.execute(
            f"UPDATE {table} SET password = ? WHERE username = ?;",
            (new_hashed_password, username),
        )
        if cur.rowcount == 0:
            raise ValueError("User not found.")
        conn.commit()


def get_user_password_hash(
    username: str, db_path: str = DB_PATH, table: str = TABLE
) -> Optional[str]:
    """Get user password hash."""
    with get_conn(db_path) as conn:
        cur = conn.execute(
            f"SELECT password FROM {table} WHERE username = ?;", (username,)
        )
        row = cur.fetchone()
        return row["password"] if row else None
