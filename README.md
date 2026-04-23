# Blogicum FastAPI
 **FastAPI** + **SQLAlchemy** вместо **DJANGO**.


## Запуск в Docker (рекомендуется)

```bash
# 1. Скопировать пример переменных окружения
cp .env.example .env

# 2. Собрать и запустить контейнеры
docker compose up --build
```

Контейнер `web` автоматически:

- дожидается готовности контейнера `db` (Postgres 16),
- применяет миграции Alembic (`alembic upgrade head`),
- запускает Uvicorn на `0.0.0.0:8000`.

Логи действий пользователя пишутся в stdout контейнера и в файл `logs/blogicum.log`
(примонтирован в хост-директорию `./logs`).

После запуска:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

Остановить:

```bash
docker compose down           # оставить данные
docker compose down -v        # удалить и данные Postgres
```

## Локальный запуск без Docker

```bash
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env              # при необходимости указать SQLite
# DATABASE_URL=sqlite:///./blogicum.db

alembic upgrade head
uvicorn app.main:app --reload
```

## Переменные окружения (Pydantic Settings)

Читаются из `.env` (см. `.env.example`) или из окружения процесса. Основные:

| Переменная | По умолчанию | Описание |
|---|---|---|
| `APP_NAME` | `Blogicum API` | Название приложения |
| `APP_VERSION` | `1.0.0` | Версия приложения |
| `DEBUG` | `False` | Режим отладки FastAPI |
| `DATABASE_URL` | `sqlite:///./blogicum.db` | SQLAlchemy URL БД |
| `SECRET_KEY` | `change_me_...` | Секрет для подписи JWT |
| `ALGORITHM` | `HS256` | Алгоритм JWT |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `60` | Время жизни токена |
| `LOG_LEVEL` | `INFO` | Уровень логирования |
| `LOG_FILE` | `logs/blogicum.log` | Файл логов |

## Логирование действий пользователя

Middleware `UserActionLoggingMiddleware` на каждый HTTP-запрос пишет строку вида:

```
2026-04-17 12:00:00 | INFO    | blogicum | user=alice ip=172.19.0.1 POST /posts/ -> 201 18.5ms
```

Имя пользователя извлекается из JWT (Bearer-токен в заголовке `Authorization`);
для неавторизованных запросов пишется `anonymous`.

Логи дублируются в stdout и в ротируемый файл `LOG_FILE`
(5 МБ × 5 файлов, `RotatingFileHandler`).

## Стек

- [FastAPI](https://fastapi.tiangolo.com/) — веб-фреймворк
- [SQLAlchemy 2.x](https://docs.sqlalchemy.org/) — ORM
- [Pydantic v2](https://docs.pydantic.dev/) + `pydantic-settings` — валидация и настройки
- [Uvicorn](https://www.uvicorn.org/) — ASGI-сервер
- [Alembic](https://alembic.sqlalchemy.org/) — миграции
- PostgreSQL 16 (в Docker) / SQLite (локально)

## Миграции Alembic вручную

```bash
alembic revision --autogenerate -m "create all tables"
alembic upgrade head
```
