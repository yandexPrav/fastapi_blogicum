"""CRUD endpoints for User."""

from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api_errors import to_http_exception
from app.errors import AppError
from app import schemas
from app.database import get_db
from app.repositories.users import UserRepository
from app.use_cases.users import UserUseCase

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[schemas.UserOut], summary="Список пользователей")
def list_users(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    """Вернуть список всех пользователей."""
    try:
        return UserUseCase(UserRepository(db)).list_users(skip=skip, limit=limit)
    except AppError as exc:
        raise to_http_exception(exc) from exc


@router.get("/{user_id}", response_model=schemas.UserOut, summary="Получить пользователя")
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Вернуть пользователя по ID."""
    try:
        return UserUseCase(UserRepository(db)).get_user(user_id)
    except AppError as exc:
        raise to_http_exception(exc) from exc


@router.post("/", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED,
             summary="Создать пользователя")
def create_user(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    """Создать нового пользователя."""
    try:
        user_payload = {
            "username": payload.username,
            "email": payload.email,
            "first_name": payload.first_name,
            "last_name": payload.last_name,
            "bio": payload.bio,
            "hashed_password": f"hashed_{payload.password}",
        }
        return UserUseCase(UserRepository(db)).create_user(user_payload)
    except AppError as exc:
        raise to_http_exception(exc) from exc


@router.put("/{user_id}", response_model=schemas.UserOut, summary="Обновить пользователя")
def update_user(user_id: int, payload: schemas.UserUpdate,
                db: Session = Depends(get_db)):
    """Частично обновить данные пользователя."""
    try:
        update_data = payload.model_dump(exclude_unset=True)
        return UserUseCase(UserRepository(db)).update_user(user_id, update_data)
    except AppError as exc:
        raise to_http_exception(exc) from exc


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Удалить пользователя")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Удалить пользователя по ID."""
    try:
        UserUseCase(UserRepository(db)).delete_user(user_id)
    except AppError as exc:
        raise to_http_exception(exc) from exc
