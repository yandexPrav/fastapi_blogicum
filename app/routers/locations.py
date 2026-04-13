"""CRUD endpoints for Location."""

from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api_errors import to_http_exception
from app import schemas
from app.database import get_db
from app.errors import AppError
from app.repositories.locations import LocationRepository
from app.use_cases.locations import LocationUseCase

router = APIRouter(prefix="/locations", tags=["Locations"])


@router.get("/", response_model=List[schemas.LocationOut],
            summary="Список местоположений")
def list_locations(skip: int = 0, limit: int = 20,
                   db: Session = Depends(get_db)):
    """Вернуть список всех местоположений."""
    try:
        return LocationUseCase(LocationRepository(db)).list_locations(
            skip=skip, limit=limit
        )
    except AppError as exc:
        raise to_http_exception(exc) from exc


@router.get("/{location_id}", response_model=schemas.LocationOut,
            summary="Получить местоположение")
def get_location(location_id: int, db: Session = Depends(get_db)):
    """Вернуть местоположение по ID."""
    try:
        return LocationUseCase(LocationRepository(db)).get_location(location_id)
    except AppError as exc:
        raise to_http_exception(exc) from exc


@router.post("/", response_model=schemas.LocationOut,
             status_code=status.HTTP_201_CREATED,
             summary="Создать местоположение")
def create_location(payload: schemas.LocationCreate,
                    db: Session = Depends(get_db)):
    """Создать новое местоположение."""
    try:
        return LocationUseCase(LocationRepository(db)).create_location(
            payload.model_dump()
        )
    except AppError as exc:
        raise to_http_exception(exc) from exc


@router.put("/{location_id}", response_model=schemas.LocationOut,
            summary="Обновить местоположение")
def update_location(location_id: int, payload: schemas.LocationUpdate,
                    db: Session = Depends(get_db)):
    """Частично обновить местоположение."""
    try:
        return LocationUseCase(LocationRepository(db)).update_location(
            location_id, payload.model_dump(exclude_unset=True)
        )
    except AppError as exc:
        raise to_http_exception(exc) from exc


@router.delete("/{location_id}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Удалить местоположение")
def delete_location(location_id: int, db: Session = Depends(get_db)):
    """Удалить местоположение по ID."""
    try:
        LocationUseCase(LocationRepository(db)).delete_location(location_id)
    except AppError as exc:
        raise to_http_exception(exc) from exc
