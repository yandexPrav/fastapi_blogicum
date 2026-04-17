"""CRUD endpoints for Post."""

from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.auth import get_current_user
from app.api_errors import to_http_exception
from app import schemas
from app.database import get_db
from app.errors import AppError
from app.repositories.posts import PostRepository
from app.repositories.users import UserRepository
from app.use_cases.posts import PostUseCase

router = APIRouter(
    prefix="/posts",
    tags=["Posts"],
    dependencies=[Depends(get_current_user)],
)


@router.get("/", response_model=List[schemas.PostOut],
            summary="Список публикаций")
def list_posts(
    skip: int = 0,
    limit: int = 20,
    published_only: bool = False,
    db: Session = Depends(get_db),
):
    """Вернуть список публикаций. При published_only=true — только опубликованные."""
    try:
        use_case = PostUseCase(PostRepository(db), UserRepository(db))
        return use_case.list_posts(skip=skip, limit=limit, published_only=published_only)
    except AppError as exc:
        raise to_http_exception(exc) from exc


@router.get("/{post_id}", response_model=schemas.PostDetail,
            summary="Получить публикацию")
def get_post(post_id: int, db: Session = Depends(get_db)):
    """Вернуть публикацию по ID со связанными автором, категорией, местом и комментариями."""
    try:
        use_case = PostUseCase(PostRepository(db), UserRepository(db))
        return use_case.get_post(post_id)
    except AppError as exc:
        raise to_http_exception(exc) from exc


@router.post("/", response_model=schemas.PostOut,
             status_code=status.HTTP_201_CREATED,
             summary="Создать публикацию")
def create_post(payload: schemas.PostCreate, db: Session = Depends(get_db)):
    """Создать новую публикацию."""
    try:
        use_case = PostUseCase(PostRepository(db), UserRepository(db))
        return use_case.create_post(payload.model_dump())
    except AppError as exc:
        raise to_http_exception(exc) from exc


@router.put("/{post_id}", response_model=schemas.PostOut,
            summary="Обновить публикацию")
def update_post(post_id: int, payload: schemas.PostUpdate,
                db: Session = Depends(get_db)):
    """Частично обновить публикацию."""
    try:
        use_case = PostUseCase(PostRepository(db), UserRepository(db))
        return use_case.update_post(post_id, payload.model_dump(exclude_unset=True))
    except AppError as exc:
        raise to_http_exception(exc) from exc


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Удалить публикацию")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    """Удалить публикацию по ID (комментарии удаляются каскадно)."""
    try:
        use_case = PostUseCase(PostRepository(db), UserRepository(db))
        use_case.delete_post(post_id)
    except AppError as exc:
        raise to_http_exception(exc) from exc
