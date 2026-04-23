"""
FastAPI Blogicum — рефакторинг Django-проекта.

Запуск:
    uvicorn app.main:app --reload

Документация:
    http://127.0.0.1:8000/docs   — Swagger UI
    http://127.0.0.1:8000/redoc  — ReDoc
"""

from fastapi import FastAPI

from app.config import settings
from app.logging_config import get_logger
from app.middleware import UserActionLoggingMiddleware
from app.routers import auth, categories, comments, locations, posts, users

logger = get_logger()

app = FastAPI(
    title=settings.app_name,
    description=(
        "REST API на FastAPI, воспроизводящий модели Django-блога "
        "(спринты 1–8): Category, Location, Post, Comment, User."
    ),
    version=settings.app_version,
    debug=settings.debug,
)

app.add_middleware(UserActionLoggingMiddleware)

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(categories.router)
app.include_router(locations.router)
app.include_router(posts.router)
app.include_router(comments.router)


@app.on_event("startup")
def _on_startup() -> None:
    logger.info("Приложение %s v%s запущено", settings.app_name, settings.app_version)


@app.on_event("shutdown")
def _on_shutdown() -> None:
    logger.info("Приложение %s остановлено", settings.app_name)


@app.get("/", tags=["Root"], summary="Корневой эндпоинт")
def root():
    """Проверка работоспособности API."""
    return {
        "message": "Blogicum FastAPI работает!",
        "docs": "/docs",
        "redoc": "/redoc",
    }
