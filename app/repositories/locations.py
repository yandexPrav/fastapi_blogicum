"""Location repository."""

from sqlalchemy.orm import Session

from app import models
from app.repositories.utils import db_call


class LocationRepository:
    """Repository for location CRUD operations."""

    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 20):
        return db_call(
            "locations.get_all",
            lambda: self.db.query(models.Location).offset(skip).limit(limit).all(),
        )

    def get_by_id(self, location_id: int):
        return db_call(
            "locations.get_by_id",
            lambda: self.db.query(models.Location)
            .filter(models.Location.id == location_id)
            .first(),
        )

    def create(self, payload):
        def _create():
            location = models.Location(**payload)
            self.db.add(location)
            self.db.commit()
            self.db.refresh(location)
            return location

        return db_call("locations.create", _create)

    def update(self, location: models.Location, payload):
        def _update():
            for field, value in payload.items():
                setattr(location, field, value)
            self.db.commit()
            self.db.refresh(location)
            return location

        return db_call("locations.update", _update)

    def delete(self, location: models.Location):
        return db_call(
            "locations.delete",
            lambda: (self.db.delete(location), self.db.commit()),
        )

