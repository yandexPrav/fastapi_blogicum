"""User repository."""

from pydantic import BaseModel, ValidationError, field_validator
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app import models
from app.errors import InfrastructureError
from app.repositories.utils import db_call


class UserCreatePayload(BaseModel):
    """Целевая проверка pydantic предназначена только для создания полезной нагрузки."""

    username: str

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        cleaned = value.strip()
        if len(cleaned) < 3:
            raise ValueError("username должен содержать минимум 3 символа")
        return cleaned

class UserRepository:
    """Repository for user CRUD operations."""

    def __init__(self, db: Session):
        self.db = db

    def get_all(self, skip: int = 0, limit: int = 20):
        return db_call(
            "users.get_all",
            lambda: self.db.query(models.User).offset(skip).limit(limit).all(),
        )

    def get_by_id(self, user_id: int):
        return db_call(
            "users.get_by_id",
            lambda: self.db.query(models.User).filter(models.User.id == user_id).first(),
        )

    def get_by_username_or_email(self, username: str, email: str):
        return db_call(
            "users.get_by_username_or_email",
            lambda: self.db.query(models.User).filter(
                or_(models.User.username == username, models.User.email == email)
            ).first(),
        )

    def get_by_username(self, username: str):
        return db_call(
            "users.get_by_username",
            lambda: self.db.query(models.User)
            .filter(models.User.username == username)
            .first(),
        )

    def create(self, payload):
        try:
            validated_create = UserCreatePayload.model_validate(payload)
        except ValidationError as exc:
            raise InfrastructureError(
                "Ошибка валидации payload для создания пользователя",
                details={"operation": "users.create", "errors": exc.errors()},
            ) from exc

        def _create():
            payload["username"] = validated_create.username
            user = models.User(**payload)
            self.db.add(user)
            self.db.commit()
            self.db.refresh(user)
            return user

        return db_call("users.create", _create)

    def update(self, user: models.User, payload):
        def _update():
            for field, value in payload.items():
                setattr(user, field, value)
            self.db.commit()
            self.db.refresh(user)
            return user

        return db_call("users.update", _update)

    def delete(self, user: models.User):
        return db_call("users.delete", lambda: (self.db.delete(user), self.db.commit()))

