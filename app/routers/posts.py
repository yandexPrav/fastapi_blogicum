"""CRUD endpoints for Post."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[schemas.PostOut],
            summary="Список публикаций")
def list_posts(
    skip: int = 0,
    limit: int = 20,
    published_only: bool = False,
    db: Session = Depends(get_db),
):
    """Вернуть список публикаций. При published_only=true — только опубликованные."""
    query = db.query(models.Post)
    if published_only:
        query = query.filter(models.Post.is_published.is_(True))
    return query.order_by(models.Post.pub_date.desc()).offset(skip).limit(limit).all()


@router.get("/{post_id}", response_model=schemas.PostDetail,
            summary="Получить публикацию")
def get_post(post_id: int, db: Session = Depends(get_db)):
    """Вернуть публикацию по ID со связанными автором, категорией, местом и комментариями."""
    post = (
        db.query(models.Post)
        .options(
            joinedload(models.Post.author),
            joinedload(models.Post.category),
            joinedload(models.Post.location),
            joinedload(models.Post.comments),
        )
        .filter(models.Post.id == post_id)
        .first()
    )
    if not post:
        raise HTTPException(status_code=404, detail="Публикация не найдена")
    return post


@router.post("/", response_model=schemas.PostOut,
             status_code=status.HTTP_201_CREATED,
             summary="Создать публикацию")
def create_post(payload: schemas.PostCreate, db: Session = Depends(get_db)):
    """Создать новую публикацию."""
    # Проверяем существование автора
    author = db.query(models.User).filter(
        models.User.id == payload.author_id
    ).first()
    if not author:
        raise HTTPException(status_code=404, detail="Автор не найден")

    post = models.Post(**payload.model_dump())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.put("/{post_id}", response_model=schemas.PostOut,
            summary="Обновить публикацию")
def update_post(post_id: int, payload: schemas.PostUpdate,
                db: Session = Depends(get_db)):
    """Частично обновить публикацию."""
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Публикация не найдена")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(post, field, value)
    db.commit()
    db.refresh(post)
    return post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Удалить публикацию")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    """Удалить публикацию по ID (комментарии удаляются каскадно)."""
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Публикация не найдена")
    db.delete(post)
    db.commit()
