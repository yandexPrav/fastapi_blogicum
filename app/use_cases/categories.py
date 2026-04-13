"""Category domain use-cases."""

from app.errors import DomainConflictError, DomainNotFoundError, InfrastructureError
from app.repositories.categories import CategoryRepository
from app.use_cases.helpers import enrich_infrastructure_error


class CategoryUseCase:
    def __init__(self, repo: CategoryRepository):
        self.repo = repo

    def list_categories(self, *, skip: int = 0, limit: int = 20):
        try:
            return self.repo.get_all(skip=skip, limit=limit)
        except InfrastructureError as exc:
            raise enrich_infrastructure_error(
                exc, entity="category", action="list"
            ) from exc

    def get_category(self, category_id: int):
        try:
            category = self.repo.get_by_id(category_id)
            if not category:
                raise DomainNotFoundError(
                    "Категория не найдена",
                    details={"entity": "category", "id": category_id},
                )
            return category
        except InfrastructureError as exc:
            raise enrich_infrastructure_error(
                exc, entity="category", action="get", extra={"id": category_id}
            ) from exc

    def create_category(self, payload: dict):
        try:
            if self.repo.get_by_slug(payload["slug"]):
                raise DomainConflictError(
                    "Категория с таким slug уже существует",
                    details={"entity": "category", "slug": payload["slug"]},
                )
            return self.repo.create(payload)
        except InfrastructureError as exc:
            raise enrich_infrastructure_error(
                exc, entity="category", action="create"
            ) from exc

    def update_category(self, category_id: int, payload: dict):
        try:
            category = self.repo.get_by_id(category_id)
            if not category:
                raise DomainNotFoundError(
                    "Категория не найдена",
                    details={"entity": "category", "id": category_id},
                )
            return self.repo.update(category, payload)
        except InfrastructureError as exc:
            raise enrich_infrastructure_error(
                exc, entity="category", action="update", extra={"id": category_id}
            ) from exc

    def delete_category(self, category_id: int):
        try:
            category = self.repo.get_by_id(category_id)
            if not category:
                raise DomainNotFoundError(
                    "Категория не найдена",
                    details={"entity": "category", "id": category_id},
                )
            self.repo.delete(category)
        except InfrastructureError as exc:
            raise enrich_infrastructure_error(
                exc, entity="category", action="delete", extra={"id": category_id}
            ) from exc

