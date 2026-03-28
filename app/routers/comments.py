"""CRUD endpoints for Comment."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.get("/", response_model=List[schemas.CommentOut],
            summary="Список комментариев")
def list_comments(
    post_id: int | None = None,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
):
    """Вернуть список комментариев. Можно фильтровать по post_id."""
    query = db.query(models.Comment)
    if post_id is not None:
        query = query.filter(models.Comment.post_id == post_id)
    return query.order_by(models.Comment.created_at).offset(skip).limit(limit).all()


@router.get("/{comment_id}", response_model=schemas.CommentOut,
            summary="Получить комментарий")
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    """Вернуть комментарий по ID."""
    comment = db.query(models.Comment).filter(
        models.Comment.id == comment_id
    ).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Комментарий не найден")
    return comment


@router.post("/", response_model=schemas.CommentOut,
             status_code=status.HTTP_201_CREATED,
             summary="Создать комментарий")
def create_comment(payload: schemas.CommentCreate,
                   db: Session = Depends(get_db)):
    """Добавить комментарий к публикации."""
    post = db.query(models.Post).filter(
        models.Post.id == payload.post_id
    ).first()
    if not post:
        raise HTTPException(status_code=404, detail="Публикация не найдена")
    author = db.query(models.User).filter(
        models.User.id == payload.author_id
    ).first()
    if not author:
        raise HTTPException(status_code=404, detail="Автор не найден")

    comment = models.Comment(**payload.model_dump())
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


@router.put("/{comment_id}", response_model=schemas.CommentOut,
            summary="Обновить комментарий")
def update_comment(comment_id: int, payload: schemas.CommentUpdate,
                   db: Session = Depends(get_db)):
    """Обновить текст комментария."""
    comment = db.query(models.Comment).filter(
        models.Comment.id == comment_id
    ).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Комментарий не найден")
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(comment, field, value)
    db.commit()
    db.refresh(comment)
    return comment


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Удалить комментарий")
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    """Удалить комментарий по ID."""
    comment = db.query(models.Comment).filter(
        models.Comment.id == comment_id
    ).first()
    if not comment:
        raise HTTPException(status_code=404, detail="Комментарий не найден")
    db.delete(comment)
    db.commit()
