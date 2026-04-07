"""CRUD endpoints for Post."""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_db
from app.repositories.posts import PostRepository
from app.repositories.users import UserRepository

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
    return PostRepository(db).get_all(
        skip=skip, limit=limit, published_only=published_only
    )


@router.get("/{post_id}", response_model=schemas.PostDetail,
            summary="Получить публикацию")
def get_post(post_id: int, db: Session = Depends(get_db)):
    """Вернуть публикацию по ID со связанными автором, категорией, местом и комментариями."""
    post = PostRepository(db).get_detailed_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Публикация не найдена")
    return post


@router.post("/", response_model=schemas.PostOut,
             status_code=status.HTTP_201_CREATED,
             summary="Создать публикацию")
def create_post(payload: schemas.PostCreate, db: Session = Depends(get_db)):
    """Создать новую публикацию."""
    # Проверяем существование автора
    author = UserRepository(db).get_by_id(payload.author_id)
    if not author:
        raise HTTPException(status_code=404, detail="Автор не найден")
    return PostRepository(db).create(payload.model_dump())


@router.put("/{post_id}", response_model=schemas.PostOut,
            summary="Обновить публикацию")
def update_post(post_id: int, payload: schemas.PostUpdate,
                db: Session = Depends(get_db)):
    """Частично обновить публикацию."""
    repo = PostRepository(db)
    post = repo.get_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Публикация не найдена")
    return repo.update(post, payload.model_dump(exclude_unset=True))


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Удалить публикацию")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    """Удалить публикацию по ID (комментарии удаляются каскадно)."""
    repo = PostRepository(db)
    post = repo.get_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Публикация не найдена")
    repo.delete(post)
