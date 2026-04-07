# Blogicum FastAPI
 **FastAPI** + **SQLAlchemy** вместо **DJANGO**.


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
