"""Helpers for domain error enrichment."""

from app.errors import DomainError, InfrastructureError


def enrich_infrastructure_error(
    error: InfrastructureError,
    *,
    entity: str,
    action: str,
    extra: dict | None = None,
) -> DomainError:
    """Build domain error with context from infrastructure failure."""
    details = {"entity": entity, "action": action}
    if error.details:
        details.update(error.details)
    if extra:
        details.update(extra)
    return DomainError(
        f"Не удалось выполнить операцию '{action}' для сущности '{entity}'",
        status_code=500,
        code="domain_infrastructure_failure",
        details=details,
    )

