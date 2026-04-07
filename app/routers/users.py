"""CRUD endpoints for User."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.repositories.users import UserRepository

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[schemas.UserOut], summary="Список пользователей")
def list_users(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    """Вернуть список всех пользователей."""
    return UserRepository(db).get_all(skip=skip, limit=limit)


@router.get("/{user_id}", response_model=schemas.UserOut, summary="Получить пользователя")
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Вернуть пользователя по ID."""
    user = UserRepository(db).get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user


@router.post("/", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED,
             summary="Создать пользователя")
def create_user(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    """Создать нового пользователя."""
    repo = UserRepository(db)
    existing = repo.get_by_username_or_email(payload.username, payload.email)
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Пользователь с таким username или email уже существует"
        )
    # В реальном проекте пароль хэшируется (например, через passlib)
    user_payload = {
        "username": payload.username,
        "email": payload.email,
        "first_name": payload.first_name,
        "last_name": payload.last_name,
        "bio": payload.bio,
        "hashed_password": f"hashed_{payload.password}",
    }
    return repo.create(user_payload)


@router.put("/{user_id}", response_model=schemas.UserOut, summary="Обновить пользователя")
def update_user(user_id: int, payload: schemas.UserUpdate,
                db: Session = Depends(get_db)):
    """Частично обновить данные пользователя."""
    repo = UserRepository(db)
    user = repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    update_data = payload.model_dump(exclude_unset=True)
    return repo.update(user, update_data)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Удалить пользователя")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Удалить пользователя по ID."""
    repo = UserRepository(db)
    user = repo.get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    repo.delete(user)
