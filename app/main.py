"""
FastAPI Blogicum — рефакторинг Django-проекта (блогicum, спринты 1–8).

Запуск:
    uvicorn app.main:app --reload

Документация:
    http://127.0.0.1:8000/docs   — Swagger UI
    http://127.0.0.1:8000/redoc  — ReDoc
"""

from fastapi import FastAPI

from app.database import Base, engine
from app.routers import categories, comments, locations, posts, users

# Создаём таблицы в БД при старте (в production используйте Alembic)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Blogicum API",
    description=(
        "REST API на FastAPI, воспроизводящий модели Django-блога "
        "(спринты 1–8): Category, Location, Post, Comment, User."
    ),
    version="1.0.0",
)

# Подключаем роутеры
app.include_router(users.router)
app.include_router(categories.router)
app.include_router(locations.router)
app.include_router(posts.router)
app.include_router(comments.router)


@app.get("/", tags=["Root"], summary="Корневой эндпоинт")
def root():
    """Проверка работоспособности API."""
    return {
        "message": "Blogicum FastAPI работает!",
        "docs": "/docs",
        "redoc": "/redoc",
    }
