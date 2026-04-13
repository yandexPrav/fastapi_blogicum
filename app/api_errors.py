"""Helpers for converting domain errors to HTTP errors."""

from fastapi import HTTPException

from app.errors import AppError


def to_http_exception(error: AppError) -> HTTPException:
    """Convert structured app error to FastAPI HTTPException."""
    detail = {"message": error.message, "code": error.code}
    if error.details:
        detail["details"] = error.details
    return HTTPException(status_code=error.status_code, detail=detail)

