# Streamlit x LiteLLM x MLFlow

LiteLLM as LLM Proxy, MLFlow for LLM Tracing and Prompt Management

## Features

- 🔐 **Authentication System**: SQLite-based user authentication with bcrypt password hashing
- 🚀 **Multi-page Navigation**: Streamlit navigation with authentication-protected pages
- 💬 **Chat Interface**: Simple chat page for LLM interactions
- 👤 **User Management**: Registration, login, and password change functionality

## Authentication

The app includes a complete authentication system with:

- User registration and login
- Password change functionality
- SQLite database backend
- Bcrypt password hashing
- Session management with cookies

### Database

User data is stored in `users.db` with the following schema:

```sql
CREATE TABLE sa_users (
    user_id     INTEGER PRIMARY KEY AUTOINCREMENT,
    username    TEXT UNIQUE NOT NULL,
    name        TEXT NOT NULL,
    email       TEXT NOT NULL,
    password    TEXT NOT NULL,       -- bcrypt hash
    role        TEXT NOT NULL DEFAULT 'user',
    created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Project Structure

```
src/streamlit_litellm_mlflow/
├── __init__.py              # Package exports
└── auth/                    # Authentication module
    ├── __init__.py          # Auth module exports
    ├── types.py             # Type definitions
    ├── database.py          # Database operations
    ├── security.py          # Password hashing utilities
    ├── authenticator.py     # Streamlit-authenticator integration
    └── ui.py                # UI components (forms)

pages/
└── 1_Simplest_Chat.py       # Chat page

main.py                      # Main application entry point
```

## Usage

1. Install dependencies:
   ```bash
   uv sync
   ```

2. Run the application:
   ```bash
   streamlit run main.py
   ```

3. Register a new account or login with existing credentials

4. Access the chat page through the navigation menu

## Todo

- [ ] Docker Compose
- [ ] Integrate LiteLLM proxy functionality
- [ ] Add MLFlow tracing and prompt management
- [ ] Enhance chat interface with LLM integration
