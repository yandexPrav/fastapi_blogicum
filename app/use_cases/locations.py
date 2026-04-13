"""Location domain use-cases."""

from app.errors import DomainNotFoundError, InfrastructureError
from app.repositories.locations import LocationRepository
from app.use_cases.helpers import enrich_infrastructure_error


class LocationUseCase:
    def __init__(self, repo: LocationRepository):
        self.repo = repo

    def list_locations(self, *, skip: int = 0, limit: int = 20):
        try:
            return self.repo.get_all(skip=skip, limit=limit)
        except InfrastructureError as exc:
            raise enrich_infrastructure_error(
                exc, entity="location", action="list"
            ) from exc

    def get_location(self, location_id: int):
        try:
            location = self.repo.get_by_id(location_id)
            if not location:
                raise DomainNotFoundError(
                    "Местоположение не найдено",
                    details={"entity": "location", "id": location_id},
                )
            return location
        except InfrastructureError as exc:
            raise enrich_infrastructure_error(
                exc, entity="location", action="get", extra={"id": location_id}
            ) from exc

    def create_location(self, payload: dict):
        try:
            return self.repo.create(payload)
        except InfrastructureError as exc:
            raise enrich_infrastructure_error(
                exc, entity="location", action="create"
            ) from exc

    def update_location(self, location_id: int, payload: dict):
        try:
            location = self.repo.get_by_id(location_id)
            if not location:
                raise DomainNotFoundError(
                    "Местоположение не найдено",
                    details={"entity": "location", "id": location_id},
                )
            return self.repo.update(location, payload)
        except InfrastructureError as exc:
            raise enrich_infrastructure_error(
                exc, entity="location", action="update", extra={"id": location_id}
            ) from exc

    def delete_location(self, location_id: int):
        try:
            location = self.repo.get_by_id(location_id)
            if not location:
                raise DomainNotFoundError(
                    "Местоположение не найдено",
                    details={"entity": "location", "id": location_id},
                )
            self.repo.delete(location)
        except InfrastructureError as exc:
            raise enrich_infrastructure_error(
                exc, entity="location", action="delete", extra={"id": location_id}
            ) from exc

