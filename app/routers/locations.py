"""CRUD endpoints for Location."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.repositories.locations import LocationRepository

router = APIRouter(prefix="/locations", tags=["Locations"])


@router.get("/", response_model=List[schemas.LocationOut],
            summary="Список местоположений")
def list_locations(skip: int = 0, limit: int = 20,
                   db: Session = Depends(get_db)):
    """Вернуть список всех местоположений."""
    return LocationRepository(db).get_all(skip=skip, limit=limit)


@router.get("/{location_id}", response_model=schemas.LocationOut,
            summary="Получить местоположение")
def get_location(location_id: int, db: Session = Depends(get_db)):
    """Вернуть местоположение по ID."""
    repo = LocationRepository(db)
    location = repo.get_by_id(location_id)
    if not location:
        raise HTTPException(status_code=404,
                            detail="Местоположение не найдено")
    return location


@router.post("/", response_model=schemas.LocationOut,
             status_code=status.HTTP_201_CREATED,
             summary="Создать местоположение")
def create_location(payload: schemas.LocationCreate,
                    db: Session = Depends(get_db)):
    """Создать новое местоположение."""
    return LocationRepository(db).create(payload.model_dump())


@router.put("/{location_id}", response_model=schemas.LocationOut,
            summary="Обновить местоположение")
def update_location(location_id: int, payload: schemas.LocationUpdate,
                    db: Session = Depends(get_db)):
    """Частично обновить местоположение."""
    repo = LocationRepository(db)
    location = repo.get_by_id(location_id)
    if not location:
        raise HTTPException(status_code=404,
                            detail="Местоположение не найдено")
    return repo.update(location, payload.model_dump(exclude_unset=True))


@router.delete("/{location_id}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Удалить местоположение")
def delete_location(location_id: int, db: Session = Depends(get_db)):
    """Удалить местоположение по ID."""
    repo = LocationRepository(db)
    location = repo.get_by_id(location_id)
    if not location:
        raise HTTPException(status_code=404,
                            detail="Местоположение не найдено")
    repo.delete(location)
