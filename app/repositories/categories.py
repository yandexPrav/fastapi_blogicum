"""Category repository."""

from sqlalchemy.orm import Session

from app import models
from app.repositories.utils import db_call


class CategoryRepository:
    """Repository for category CRUD operations."""

    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 20):
        return db_call(
            "categories.get_all",
            lambda: self.db.query(models.Category).offset(skip).limit(limit).all(),
        )

    def get_by_id(self, category_id: int):
        return db_call(
            "categories.get_by_id",
            lambda: self.db.query(models.Category)
            .filter(models.Category.id == category_id)
            .first(),
        )

    def get_by_slug(self, slug: str):
        return db_call(
            "categories.get_by_slug",
            lambda: self.db.query(models.Category)
            .filter(models.Category.slug == slug)
            .first(),
        )

    def create(self, payload):
        def _create():
            category = models.Category(**payload)
            self.db.add(category)
            self.db.commit()
            self.db.refresh(category)
            return category

        return db_call("categories.create", _create)

    def update(self, category: models.Category, payload):
        def _update():
            for field, value in payload.items():
                setattr(category, field, value)
            self.db.commit()
            self.db.refresh(category)
            return category

        return db_call("categories.update", _update)

    def delete(self, category: models.Category):
        return db_call(
            "categories.delete",
            lambda: (self.db.delete(category), self.db.commit()),
        )

