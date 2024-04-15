from datetime import timedelta
from typing import Any, Optional
from uuid import UUID, uuid4

from fastapi import HTTPException
from fastapi_sessions.backends.implementations import InMemoryBackend
from fastapi_sessions.frontends.implementations import CookieParameters, SessionCookie
from fastapi_sessions.session_verifier import SessionVerifier
from pydantic import BaseModel


class SessionData(BaseModel):
    user_id: str = uuid4()
    chain: Optional[Any] = None
    chain_exercise: Optional[Any] = None
    # Add other fields as needed


SESSION_SECRET_KEY = "a_very_secret_key_change_me"

session_backend = InMemoryBackend[UUID, SessionData]()
session_cookie = SessionCookie(
    cookie_name="cookie",
    identifier="general_verifier",
    auto_error=True,
    secret_key="DONOTUSE",
    cookie_params=CookieParameters(),
)


class BasicVerifier(SessionVerifier[UUID, SessionData]):
    def __init__(
        self,
        *,
        identifier: str,
        auto_error: bool,
        backend: InMemoryBackend[UUID, SessionData],
        auth_http_exception: HTTPException,
    ):
        self._identifier = identifier
        self._auto_error = auto_error
        self._backend = backend
        self._auth_http_exception = auth_http_exception

    @property
    def identifier(self):
        return self._identifier

    @property
    def backend(self):
        return self._backend

    @property
    def auto_error(self):
        return self._auto_error

    @property
    def auth_http_exception(self):
        return self._auth_http_exception

    def verify_session(self, model: SessionData) -> bool:
        """If the session exists, it is valid"""
        print(f"verifying session {model.user_id}")
        session_exists = self._backend.get(model.user_id)
        return True

    async def create_session(self) -> SessionData:
        """Create a new session"""
        data = SessionData()
        await self._backend.create(data.user_id, data)
        return data


verifier = BasicVerifier(
    identifier="general_verifier",
    auto_error=True,
    backend=session_backend,
    auth_http_exception=HTTPException(status_code=403, detail="invalid session"),
)
