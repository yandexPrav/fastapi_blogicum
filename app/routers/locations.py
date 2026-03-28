"""CRUD endpoints for Location."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/locations", tags=["Locations"])


@router.get("/", response_model=List[schemas.LocationOut],
            summary="Список местоположений")
def list_locations(skip: int = 0, limit: int = 20,
                   db: Session = Depends(get_db)):
    """Вернуть список всех местоположений."""
    return db.query(models.Location).offset(skip).limit(limit).all()


@router.get("/{location_id}", response_model=schemas.LocationOut,
            summary="Получить местоположение")
def get_location(location_id: int, db: Session = Depends(get_db)):
    """Вернуть местоположение по ID."""
    location = db.query(models.Location).filter(
        models.Location.id == location_id
    ).first()
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
    location = models.Location(**payload.model_dump())
    db.add(location)
    db.commit()
    db.refresh(location)
    return location


@router.put("/{location_id}", response_model=schemas.LocationOut,
            summary="Обновить местоположение")
def update_location(location_id: int, payload: schemas.LocationUpdate,
                    db: Session = Depends(get_db)):
    """Частично обновить местоположение."""
    location = db.query(models.Location).filter(
        models.Location.id == location_id
    ).first()
    if not location:
        raise HTTPException(status_code=404,
                            detail="Местоположение не найдено")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(location, field, value)
    db.commit()
    db.refresh(location)
    return location


@router.delete("/{location_id}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Удалить местоположение")
def delete_location(location_id: int, db: Session = Depends(get_db)):
    """Удалить местоположение по ID."""
    location = db.query(models.Location).filter(
        models.Location.id == location_id
    ).first()
    if not location:
        raise HTTPException(status_code=404,
                            detail="Местоположение не найдено")
    db.delete(location)
    db.commit()
