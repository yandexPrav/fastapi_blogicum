"""CRUD endpoints for Category."""

from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.api_errors import to_http_exception
from app import schemas
from app.database import get_db
from app.errors import AppError
from app.repositories.categories import CategoryRepository
from app.use_cases.categories import CategoryUseCase

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/", response_model=List[schemas.CategoryOut],
            summary="Список категорий")
def list_categories(skip: int = 0, limit: int = 20,
                    db: Session = Depends(get_db)):
    """Вернуть список всех категорий."""
    try:
        return CategoryUseCase(CategoryRepository(db)).list_categories(
            skip=skip, limit=limit
        )
    except AppError as exc:
        raise to_http_exception(exc) from exc


@router.get("/{category_id}", response_model=schemas.CategoryOut,
            summary="Получить категорию")
def get_category(category_id: int, db: Session = Depends(get_db)):
    """Вернуть категорию по ID."""
    try:
        return CategoryUseCase(CategoryRepository(db)).get_category(category_id)
    except AppError as exc:
        raise to_http_exception(exc) from exc


@router.post("/", response_model=schemas.CategoryOut,
             status_code=status.HTTP_201_CREATED,
             summary="Создать категорию")
def create_category(payload: schemas.CategoryCreate,
                    db: Session = Depends(get_db)):
    """Создать новую категорию."""
    try:
        return CategoryUseCase(CategoryRepository(db)).create_category(
            payload.model_dump()
        )
    except AppError as exc:
        raise to_http_exception(exc) from exc


@router.put("/{category_id}", response_model=schemas.CategoryOut,
            summary="Обновить категорию")
def update_category(category_id: int, payload: schemas.CategoryUpdate,
                    db: Session = Depends(get_db)):
    """Частично обновить категорию."""
    try:
        return CategoryUseCase(CategoryRepository(db)).update_category(
            category_id, payload.model_dump(exclude_unset=True)
        )
    except AppError as exc:
        raise to_http_exception(exc) from exc


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Удалить категорию")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    """Удалить категорию по ID."""
    try:
        CategoryUseCase(CategoryRepository(db)).delete_category(category_id)
    except AppError as exc:
        raise to_http_exception(exc) from exc
