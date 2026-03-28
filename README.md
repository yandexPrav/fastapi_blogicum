# Blogicum FastAPI

Рефакторинг Django-проекта «Blogicum» (спринты 1–8) на **FastAPI** + **SQLAlchemy**.

## Модели

| Django-модель | SQLAlchemy-таблица | Описание |
|---|---|---|
| `User` (встроенная) | `users` | Пользователи блога |
| `Category(PublishedModel)` | `categories` | Категории публикаций |
| `Location(PublishedModel)` | `locations` | Местоположения |
| `Post(PublishedModel)` | `posts` | Публикации блога |
| `Comment` | `comments` | Комментарии к публикациям |

## Эндпоинты (GET / POST / PUT / DELETE)

| Ресурс | GET (список) | GET (один) | POST | PUT | DELETE |
|---|---|---|---|---|---|
| Users | `GET /users/` | `GET /users/{id}` | `POST /users/` | `PUT /users/{id}` | `DELETE /users/{id}` |
| Categories | `GET /categories/` | `GET /categories/{id}` | `POST /categories/` | `PUT /categories/{id}` | `DELETE /categories/{id}` |
| Locations | `GET /locations/` | `GET /locations/{id}` | `POST /locations/` | `PUT /locations/{id}` | `DELETE /locations/{id}` |
| Posts | `GET /posts/` | `GET /posts/{id}` | `POST /posts/` | `PUT /posts/{id}` | `DELETE /posts/{id}` |
| Comments | `GET /comments/` | `GET /comments/{id}` | `POST /comments/` | `PUT /comments/{id}` | `DELETE /comments/{id}` |

## Как запустить

```bash
# Клонировать репозиторий
git clone <url>
cd fastapi_blogicum

# Создать и активировать виртуальное окружение
python -m venv venv
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Установить зависимости
pip install -r requirements.txt

# Запустить сервер
uvicorn app.main:app --reload
```

После запуска открыть в браузере:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## Стек

- [FastAPI](https://fastapi.tiangolo.com/) — веб-фреймворк
- [SQLAlchemy 2.x](https://docs.sqlalchemy.org/) — ORM
- [Pydantic v2](https://docs.pydantic.dev/) — валидация данных
- [Uvicorn](https://www.uvicorn.org/) — ASGI-сервер
- SQLite — база данных (файл `blogicum.db` создаётся автоматически)
