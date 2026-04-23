"""HTTP middleware: логирование действий пользователя."""

from __future__ import annotations

import time

from fastapi import Request
from jose import JWTError, jwt
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from app.config import settings
from app.logging_config import get_logger

logger = get_logger()


def _extract_username(request: Request) -> str:
    """Попытаться достать имя пользователя из JWT токена заголовка Authorization."""
    auth_header = request.headers.get("authorization", "")
    if not auth_header.lower().startswith("bearer "):
        return "anonymous"
    token = auth_header.split(" ", 1)[1].strip()
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        return payload.get("sub") or "anonymous"
    except JWTError:
        return "anonymous"


class UserActionLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware, логирующий каждое действие пользователя.

    Формат: пользователь, метод, путь, статус, длительность, IP-адрес клиента.
    """

    async def dispatch(self, request: Request, call_next) -> Response:
        start = time.perf_counter()
        username = _extract_username(request)
        client_ip = request.client.host if request.client else "-"

        try:
            response = await call_next(request)
        except Exception:
            duration_ms = (time.perf_counter() - start) * 1000
            logger.exception(
                "user=%s ip=%s %s %s -> 500 %.1fms",
                username,
                client_ip,
                request.method,
                request.url.path,
                duration_ms,
            )
            raise

        duration_ms = (time.perf_counter() - start) * 1000
        logger.info(
            "user=%s ip=%s %s %s -> %d %.1fms",
            username,
            client_ip,
            request.method,
            request.url.path,
            response.status_code,
            duration_ms,
        )
        return response
