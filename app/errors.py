"""Application error types for infrastructure, domain and API layers."""

from __future__ import annotations


class AppError(Exception):
    """Base application error with structured context."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int = 500,
        code: str = "app_error",
        details: dict | None = None,
    ):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.code = code
        self.details = details or {}


class InfrastructureError(AppError):
    """Database/infrastructure level failure."""

    def __init__(self, message: str, *, details: dict | None = None):
        super().__init__(
            message,
            status_code=500,
            code="infrastructure_error",
            details=details,
        )


class DomainError(AppError):
    """Domain/use-case level failure."""

    def __init__(
        self,
        message: str,
        *,
        status_code: int = 400,
        code: str = "domain_error",
        details: dict | None = None,
    ):
        super().__init__(message, status_code=status_code, code=code, details=details)


class DomainNotFoundError(DomainError):
    """Entity not found in domain layer."""

    def __init__(self, message: str, *, details: dict | None = None):
        super().__init__(
            message,
            status_code=404,
            code="not_found",
            details=details,
        )


class DomainConflictError(DomainError):
    """Entity conflict in domain layer."""

    def __init__(self, message: str, *, details: dict | None = None):
        super().__init__(
            message,
            status_code=409,
            code="conflict",
            details=details,
        )

