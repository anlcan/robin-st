from datetime import timedelta
from typing import Optional
from uuid import UUID
from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters
from pydantic import BaseModel

class SessionInfo(BaseModel):
    user_id: str
    username: str
    chain: Optional[Any] = None
    chain_exercise: Optional[Any] = None
    # Add other fields as needed

SESSION_SECRET_KEY = "a_very_secret_key_change_me"

session_backend = InMemoryBackend[UUID,SessionInfo]()
session_cookie = SessionCookie(
    cookie_name="cookie",
    identifier="general_verifier",
    auto_error=True,
    secret_key="DONOTUSE",
    cookie_params=CookieParameters()
)
from datetime import timedelta
from typing import Optional, Any
from uuid import UUID
from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.frontends.implementations import SessionCookie, CookieParameters
from pydantic import BaseModel

class SessionInfo(BaseModel):
    user_id: str
    username: str
    chain: Optional[Any] = None
    chain_exercise: Optional[Any] = None
    # Add other fields as needed

SESSION_SECRET_KEY = "a_very_secret_key_change_me"

session_backend = InMemoryBackend[UUID,SessionInfo]()
session_cookie = SessionCookie(
    cookie_name="cookie",
    identifier="general_verifier",
    auto_error=True,
    secret_key=SESSION_SECRET_KEY,
    cookie_params=CookieParameters()
)
