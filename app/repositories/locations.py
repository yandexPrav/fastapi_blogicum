"""Location repository."""

from sqlalchemy.orm import Session

from app import models


class LocationRepository:
    """Repository for location CRUD operations."""

    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 20):
        return self.db.query(models.Location).offset(skip).limit(limit).all()

    def get_by_id(self, location_id: int):
        return (
            self.db.query(models.Location)
            .filter(models.Location.id == location_id)
            .first()
        )

    def create(self, payload):
        location = models.Location(**payload)
        self.db.add(location)
        self.db.commit()
        self.db.refresh(location)
        return location

    def update(self, location: models.Location, payload):
        for field, value in payload.items():
            setattr(location, field, value)
        self.db.commit()
        self.db.refresh(location)
        return location

    def delete(self, location: models.Location):
        self.db.delete(location)
        self.db.commit()

