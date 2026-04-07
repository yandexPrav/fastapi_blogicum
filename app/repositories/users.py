"""User repository."""

from sqlalchemy import or_
from sqlalchemy.orm import Session

from app import models


class UserRepository:
    """Repository for user CRUD operations."""

    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 20):
        return self.db.query(models.User).offset(skip).limit(limit).all()

    def get_by_id(self, user_id: int):
        return self.db.query(models.User).filter(models.User.id == user_id).first()

    def get_by_username_or_email(self, username: str, email: str):
        return self.db.query(models.User).filter(
            or_(models.User.username == username, models.User.email == email)
        ).first()

    def create(self, payload):
        user = models.User(**payload)
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update(self, user: models.User, payload):
        for field, value in payload.items():
            setattr(user, field, value)
        self.db.commit()
        self.db.refresh(user)
        return user

    def delete(self, user: models.User):
        self.db.delete(user)
        self.db.commit()

