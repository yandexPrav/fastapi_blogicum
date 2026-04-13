"""CRUD endpoints for Comment."""

from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api_errors import to_http_exception
from app import schemas
from app.database import get_db
from app.errors import AppError
from app.repositories.comments import CommentRepository
from app.repositories.posts import PostRepository
from app.repositories.users import UserRepository
from app.use_cases.comments import CommentUseCase

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
    try:
        use_case = CommentUseCase(
            CommentRepository(db), PostRepository(db), UserRepository(db)
        )
        return use_case.list_comments(post_id=post_id, skip=skip, limit=limit)
    except AppError as exc:
        raise to_http_exception(exc) from exc


@router.get("/{comment_id}", response_model=schemas.CommentOut,
            summary="Получить комментарий")
def get_comment(comment_id: int, db: Session = Depends(get_db)):
    """Вернуть комментарий по ID."""
    try:
        use_case = CommentUseCase(
            CommentRepository(db), PostRepository(db), UserRepository(db)
        )
        return use_case.get_comment(comment_id)
    except AppError as exc:
        raise to_http_exception(exc) from exc


@router.post("/", response_model=schemas.CommentOut,
             status_code=status.HTTP_201_CREATED,
             summary="Создать комментарий")
def create_comment(payload: schemas.CommentCreate,
                   db: Session = Depends(get_db)):
    """Добавить комментарий к публикации."""
    try:
        use_case = CommentUseCase(
            CommentRepository(db), PostRepository(db), UserRepository(db)
        )
        return use_case.create_comment(payload.model_dump())
    except AppError as exc:
        raise to_http_exception(exc) from exc


@router.put("/{comment_id}", response_model=schemas.CommentOut,
            summary="Обновить комментарий")
def update_comment(comment_id: int, payload: schemas.CommentUpdate,
                   db: Session = Depends(get_db)):
    """Обновить текст комментария."""
    try:
        use_case = CommentUseCase(
            CommentRepository(db), PostRepository(db), UserRepository(db)
        )
        return use_case.update_comment(comment_id, payload.model_dump(exclude_unset=True))
    except AppError as exc:
        raise to_http_exception(exc) from exc


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Удалить комментарий")
def delete_comment(comment_id: int, db: Session = Depends(get_db)):
    """Удалить комментарий по ID."""
    try:
        use_case = CommentUseCase(
            CommentRepository(db), PostRepository(db), UserRepository(db)
        )
        use_case.delete_comment(comment_id)
    except AppError as exc:
        raise to_http_exception(exc) from exc
