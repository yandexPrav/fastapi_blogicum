"""CRUD endpoints for Category."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.repositories.categories import CategoryRepository

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=List[schemas.CategoryOut],
            summary="Список категорий")
def list_categories(skip: int = 0, limit: int = 20,
                    db: Session = Depends(get_db)):
    """Вернуть список всех категорий."""
    return CategoryRepository(db).get_all(skip=skip, limit=limit)


@router.get("/{category_id}", response_model=schemas.CategoryOut,
            summary="Получить категорию")
def get_category(category_id: int, db: Session = Depends(get_db)):
    """Вернуть категорию по ID."""
    repo = CategoryRepository(db)
    category = repo.get_by_id(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    return category


@router.post("/", response_model=schemas.CategoryOut,
             status_code=status.HTTP_201_CREATED,
             summary="Создать категорию")
def create_category(payload: schemas.CategoryCreate,
                    db: Session = Depends(get_db)):
    """Создать новую категорию."""
    repo = CategoryRepository(db)
    if repo.get_by_slug(payload.slug):
        raise HTTPException(status_code=400,
                            detail="Категория с таким slug уже существует")
    return repo.create(payload.model_dump())


@router.put("/{category_id}", response_model=schemas.CategoryOut,
            summary="Обновить категорию")
def update_category(category_id: int, payload: schemas.CategoryUpdate,
                    db: Session = Depends(get_db)):
    """Частично обновить категорию."""
    repo = CategoryRepository(db)
    category = repo.get_by_id(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    return repo.update(category, payload.model_dump(exclude_unset=True))


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Удалить категорию")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """Удалить категорию по ID."""
    repo = CategoryRepository(db)
    category = repo.get_by_id(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Категория не найдена")
    repo.delete(category)
