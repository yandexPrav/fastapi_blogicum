"""User domain use-cases."""

from app.errors import DomainConflictError, DomainNotFoundError, InfrastructureError
from app.repositories.users import UserRepository
from app.use_cases.helpers import enrich_infrastructure_error


class UserUseCase:
    """Business operations for users."""

    def __init__(self, repo: UserRepository):
        self.repo = repo

    def list_users(self, *, skip: int = 0, limit: int = 20):
        try:
            return self.repo.get_all(skip=skip, limit=limit)
        except InfrastructureError as exc:
            raise enrich_infrastructure_error(exc, entity="user", action="list") from exc

    def get_user(self, user_id: int):
        try:
            user = self.repo.get_by_id(user_id)
            if not user:
                raise DomainNotFoundError(
                    "Пользователь не найден",
                    details={"entity": "user", "id": user_id},
                )
            return user
        except InfrastructureError as exc:
            raise enrich_infrastructure_error(
                exc, entity="user", action="get", extra={"id": user_id}
            ) from exc

    def create_user(self, payload: dict):
        try:
            existing = self.repo.get_by_username_or_email(
                payload["username"], payload["email"]
            )
            if existing:
                raise DomainConflictError(
                    "Пользователь с таким username или email уже существует",
                    details={"entity": "user", "username": payload["username"]},
                )
            return self.repo.create(payload)
        except InfrastructureError as exc:
            raise enrich_infrastructure_error(exc, entity="user", action="create") from exc

    def update_user(self, user_id: int, payload: dict):
        try:
            user = self.repo.get_by_id(user_id)
            if not user:
                raise DomainNotFoundError(
                    "Пользователь не найден",
                    details={"entity": "user", "id": user_id},
                )
            return self.repo.update(user, payload)
        except InfrastructureError as exc:
            raise enrich_infrastructure_error(
                exc, entity="user", action="update", extra={"id": user_id}
            ) from exc

    def delete_user(self, user_id: int):
        try:
            user = self.repo.get_by_id(user_id)
            if not user:
                raise DomainNotFoundError(
                    "Пользователь не найден",
                    details={"entity": "user", "id": user_id},
                )
            self.repo.delete(user)
        except InfrastructureError as exc:
            raise enrich_infrastructure_error(
                exc, entity="user", action="delete", extra={"id": user_id}
            ) from exc

