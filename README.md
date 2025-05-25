# Благотворительный фонд поддержки котиков QRKot

## Описание проекта
  QRKot — это API-сервис для управления благотворительными проектами и пожертвованиями. Пользователи могут создавать пожертвования, а суперюзеры — управлять фондами. Средства автоматически распределяются между проектами.

## Установка и запуск
  Клонировать репозиторий и перейти в него в командной строке:

    git clone git@github.com:bauklu/cat_charity_fund.git
    cd cat_charity_fund

## Cоздать и активировать виртуальное окружение:

  python3 -m venv venv
  Если у вас Linux/macOS

    source venv/bin/activate

  Если у вас windows

    source venv/scripts/activate

  Установить зависимости из файла requirements.txt:

    python3 -m pip install --upgrade pip

    pip install -r requirements.txt

  Запустить приложение: uvicorn app.main:app --reload

## Использование
  
  Документация доступна по адресу:

    Swagger UI: http://127.0.0.1:8000/docs

    ReDoc: http://127.0.0.1:8000/redoc

  Для доступа к защищённым методам зарегистрируйтесь и получите JWT-токен.

## Тестирование
  
  Запустить тесты: pytest

## Стек технологий
  Python 3.11+

  FastAPI

  SQLAlchemy (async)

  SQLite (aiosqlite)

  Alembic

  Pydantic

  Pytest

## Информация об авторе:
  https://github.com/bauklu
