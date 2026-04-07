"""CRUD endpoints for Comment."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.repositories.comments import CommentRepository
from app.repositories.posts import PostRepository
from app.repositories.users import UserRepository

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
    return CommentRepository(db).get_all(post_id=post_id, skip=skip, limit=limit)


@router.get("/{comment_id}", response_model=schemas.CommentOut,
            summary="Получить комментарий")
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    """Вернуть комментарий по ID."""
    comment = CommentRepository(db).get_by_id(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Комментарий не найден")
    return comment


@router.post("/", response_model=schemas.CommentOut,
             status_code=status.HTTP_201_CREATED,
             summary="Создать комментарий")
def create_comment(payload: schemas.CommentCreate,
                   db: Session = Depends(get_db)):
    """Добавить комментарий к публикации."""
    post = PostRepository(db).get_by_id(payload.post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Публикация не найдена")
    author = UserRepository(db).get_by_id(payload.author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Автор не найден")
    return CommentRepository(db).create(payload.model_dump())


@router.put("/{comment_id}", response_model=schemas.CommentOut,
            summary="Обновить комментарий")
def update_comment(comment_id: int, payload: schemas.CommentUpdate,
                   db: Session = Depends(get_db)):
    """Обновить текст комментария."""
    repo = CommentRepository(db)
    comment = repo.get_by_id(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Комментарий не найден")
    return repo.update(comment, payload.model_dump(exclude_unset=True))


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Удалить комментарий")
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    """Удалить комментарий по ID."""
    repo = CommentRepository(db)
    comment = repo.get_by_id(comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Комментарий не найден")
    repo.delete(comment)
