"""CRUD endpoints for User."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=List[schemas.UserOut], summary="Список пользователей")
def list_users(skip: int = 0, limit: int = 20, db: Session = Depends(get_db)):
    """Вернуть список всех пользователей."""
    return db.query(models.User).offset(skip).limit(limit).all()


@router.get("/{user_id}", response_model=schemas.UserOut, summary="Получить пользователя")
def get_user(user_id: int, db: Session = Depends(get_db)):
    """Вернуть пользователя по ID."""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user


@router.post("/", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED,
             summary="Создать пользователя")
def create_user(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    """Создать нового пользователя."""
    existing = db.query(models.User).filter(
        (models.User.username == payload.username) |
        (models.User.email == payload.email)
    ).first()
    if existing:
        raise HTTPException(
            status_code=400,
            detail="Пользователь с таким username или email уже существует"
        )
    # В реальном проекте пароль хэшируется (например, через passlib)
    user = models.User(
        username=payload.username,
        email=payload.email,
        first_name=payload.first_name,
        last_name=payload.last_name,
        bio=payload.bio,
        hashed_password=f"hashed_{payload.password}",  # заглушка
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.put("/{user_id}", response_model=schemas.UserOut, summary="Обновить пользователя")
def update_user(user_id: int, payload: schemas.UserUpdate,
                db: Session = Depends(get_db)):
    """Частично обновить данные пользователя."""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Удалить пользователя")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Удалить пользователя по ID."""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    db.delete(user)
    db.commit()
