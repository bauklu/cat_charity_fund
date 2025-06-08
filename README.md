# Благотворительный фонд поддержки котиков QRKot

## Описание проекта
  QRKot — это API-сервис для управления благотворительными проектами и пожертвованиями. Пользователи могут создавать пожертвования, а суперюзеры — управлять фондами. Средства автоматически распределяются между проектами. В приложении есть возможность формирования отчёта в Google Sheets. Проекты в google-таблице сортируются по скорости сбора средств.

## Возможности

  Регистрация и аутентификация пользователей
  Создание, редактирование и удаление благотворительных проектов (только для   суперпользователей)
  Создание пожертвований
  Автоматическое распределение пожертвований между проектами
  JWT-аутентификация
  Документация Swagger и ReDoc


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


## Миграции базы данных

  Если вы используете Alembic и в проекте есть миграции, выполните их перед запуском приложения.

  Создать миграцию (если нужно):
    alembic revision --autogenerate -m "Initial migration"

  Применить миграции:
    alembic upgrade head

## Примеры запросов:
  Получение всех благотворительных проектов:
    GET /charity_project/
    Authorization: Bearer <ваш токен>

  Создание проекта (только для суперпользователя):
    POST /charity_project/

    {
      "name": "Помощь котятам",
      "description": "Сбор на корм и лечение",
      "full_amount": 10000
    }

  Создание пожертвования:
    POST /donation/

    {
      "full_amount": 1500,
      "comment": "На корм"
    }

  Статистика по скорости закрытия проектов:
    GET /charity_project/by_completion_rate/
      Возвращает отсортированный список проектов с описанием и временем сбора:
      [
        {
          "charityproject_name": "Проект A",
          "duration": "1 day, 02:30:00.000000",
          "charityproject_description": "Описание"
        },
        ...
      ]

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

  Google Sheets API

  Google Drive API

## Информация об авторе:
  Автор: Людмила Баукова 
  https://github.com/bauklu
  Email: bauklu.email@yandex.ru
