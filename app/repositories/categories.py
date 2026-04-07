"""Category repository."""

from sqlalchemy.orm import Session

from app import models


class CategoryRepository:
    """Repository for category CRUD operations."""

    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 20):
        return self.db.query(models.Category).offset(skip).limit(limit).all()

    def get_by_id(self, category_id: int):
        return (
            self.db.query(models.Category)
            .filter(models.Category.id == category_id)
            .first()
        )

    def get_by_slug(self, slug: str):
        return self.db.query(models.Category).filter(models.Category.slug == slug).first()

    def create(self, payload):
        category = models.Category(**payload)
        self.db.add(category)
        self.db.commit()
        self.db.refresh(category)
        return category

    def update(self, category: models.Category, payload):
        for field, value in payload.items():
            setattr(category, field, value)
        self.db.commit()
        self.db.refresh(category)
        return category

    def delete(self, category: models.Category):
        self.db.delete(category)
        self.db.commit()

