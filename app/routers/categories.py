"""CRUD endpoints for Category."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=List[schemas.CategoryOut],
            summary="Список категорий")
def list_categories(skip: int = 0, limit: int = 20,
                    db: Session = Depends(get_db)):
    """Вернуть список всех категорий."""
    return db.query(models.Category).offset(skip).limit(limit).all()


@router.get("/{category_id}", response_model=schemas.CategoryOut,
            summary="Получить категорию")
def get_category(category_id: int, db: Session = Depends(get_db)):
    """Вернуть категорию по ID."""
    category = db.query(models.Category).filter(
        models.Category.id == category_id
    ).first()
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    return category


@router.post("/", response_model=schemas.CategoryOut,
             status_code=status.HTTP_201_CREATED,
             summary="Создать категорию")
def create_category(payload: schemas.CategoryCreate,
                    db: Session = Depends(get_db)):
    """Создать новую категорию."""
    if db.query(models.Category).filter(
        models.Category.slug == payload.slug
    ).first():
        raise HTTPException(status_code=400,
                            detail="Категория с таким slug уже существует")
    category = models.Category(**payload.model_dump())
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


@router.put("/{category_id}", response_model=schemas.CategoryOut,
            summary="Обновить категорию")
def update_category(category_id: int, payload: schemas.CategoryUpdate,
                    db: Session = Depends(get_db)):
    """Частично обновить категорию."""
    category = db.query(models.Category).filter(
        models.Category.id == category_id
    ).first()
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(category, field, value)
    db.commit()
    db.refresh(category)
    return category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Удалить категорию")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """Удалить категорию по ID."""
    category = db.query(models.Category).filter(
        models.Category.id == category_id
    ).first()
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    db.delete(category)
    db.commit()
