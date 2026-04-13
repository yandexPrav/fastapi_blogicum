"""Repository helpers."""

from collections.abc import Callable

from sqlalchemy.exc import SQLAlchemyError

from app.errors import InfrastructureError


def db_call(operation: str, fn: Callable):
    """Execute DB operation and map SQLAlchemy errors."""
    try:
        return fn()
    except SQLAlchemyError as exc:
        raise InfrastructureError(
            "Ошибка при работе с базой данных",
            details={"operation": operation, "reason": str(exc.__class__.__name__)},
        ) from exc

