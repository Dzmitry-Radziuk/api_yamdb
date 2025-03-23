# YaMDb API  

Проект **YaMDb** собирает отзывы пользователей о различных произведениях (фильмах, книгах, песнях и т. д.).  
API реализовано с использованием Django и Django REST framework, а аутентификация – через JWT.  

## Структура проекта  

api_yamdb/
├── api/               # Основное приложение API
│   ├── common/        # Утилиты и валидаторы
│   ├── admin.py       # Настройки админки
│   ├── apps.py        # Конфигурация приложения
│   ├── exceptions.py  # Обработчики исключений
│   ├── paginations.py # Настройки пагинации
│   ├── permissions.py # Настройки прав доступа
│   ├── serializers.py # Сериализаторы API
│   ├── urls.py        # Маршрутизация API
│   ├── views.py       # Контроллеры API
│   ├── __init__.py
│   └── ...
│
├── api_yamdb/         # Основные настройки Django-проекта
│   ├── settings.py    # Конфигурация проекта
│   ├── urls.py        # Главные маршруты проекта
│   ├── wsgi.py        # Точка входа для WSGI
│   ├── asgi.py        # Точка входа для ASGI
│   ├── __init__.py
│   └── ...
│
├── reviews/           # Приложение для отзывов и комментариев
│   ├── models.py      # Модели отзывов и комментариев
│   ├── urls.py        # Маршруты приложения
│   ├── apps.py
│   ├── __init__.py
│   └── ...
│
├── titles/            # Приложение для произведений
│   ├── management/    # Команда для загрузки данных из CSV
│   │   ├── commands/
│   │   │   ├── load_csv_data.py # Скрипт загрузки данных
│   │   │   ├── __init.py__
│   │   └── ...
│   ├── models.py      # Модели произведений
│   ├── apps.py
│   ├── __init__.py
│   └── ...
│
├── users/             # Приложение для пользователей
│   ├── models.py      # Модель пользователя
│   ├── apps.py
│   ├── __init__.py
│   └── ...
│
├── static/            # Статические файлы и данные
│   ├── data/          # CSV-файлы для загрузки
│   ├── redoc.yaml     # Документация API
│   └── ...
│
├── templates/         # HTML-шаблоны
│   ├── redoc.html     # Документация в формате ReDoc
│   └── ...
│
├── manage.py          # Главный скрипт управления Django
├── .env               # Файл с переменными окружения
├── db.sqlite3         # Локальная база данных SQLite
└── requirements.txt   # Зависимости проекта

## Установка  
  
```sh
Клонируйте репозиторий:
git clone https://github.com/Dzmitry-Radziuk/api_yamdb  
cd api_yamdb  
Создайте и активируйте виртуальное окружение:
python -m venv venv  
# Windows:  
venv\Scripts\activate  
# Linux/macOS:  
source venv/bin/activate  
Установите зависимости:
pip install -r requirements.txt  
Примените миграции:
python manage.py makemigrations  
python manage.py migrate  
Создайте суперпользователя (опционально):
python manage.py createsuperuser  
Загрузка данных из CSV
Для массового импорта данных из CSV-файлов используется команда load_csv_data. CSV-файлы должны находиться в папке static/data/.
python manage.py load_csv_data  
После выполнения команды появится сообщение об успешной загрузке данных.

Запуск сервера
python manage.py runserver  
Сервер будет доступен по адресу: http://127.0.0.1:8000/

API Эндпоинты
Аутентификация:
POST /api/v1/auth/signup/  
Описание: Регистрация пользователя (отправка email и username).

POST /api/v1/auth/token/  
Описание: Получение JWT-токена (по username и confirmation_code).

Категории:
http
GET /api/v1/categories/  
Описание: Получение списка категорий (без токена).

POST /api/v1/categories/  
Описание: Создание категории (только для администраторов).

Произведения:
http
GET /api/v1/titles/  
Описание: Получение списка произведений (без токена), поддерживается фильтрация по category__slug, genre__slug, name и year.

POST /api/v1/titles/  
Описание: Добавление произведения (только для администраторов). При добавлении нельзя указывать год выпуска больше текущего.

Отзывы и комментарии:
GET /api/v1/titles/{title_id}/reviews/  
Описание: Получение отзывов для произведения (без токена).

POST /api/v1/titles/{title_id}/reviews/  
Описание: Создание отзыва (только для аутентифицированных пользователей, один отзыв на произведение).

GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/  
Описание: Получение комментариев к отзыву (без токена).

POST /api/v1/titles/{title_id}/reviews/{review_id}/comments/  
Описание: Создание комментария (только для аутентифицированных пользователей).

Полное описание API можно найти в redoc.yaml.

Примеры запросов и ответов
1. Регистрация пользователя
Запрос:
http
POST /api/v1/auth/signup/
json
{
  "username": "new_user",
  "email": "new_user@example.com"
}
Ответ:
json
{
  "username": "new_user",
  "email": "new_user@example.com"
}

2. Получение списка категорий
Запрос:
http
GET /api/v1/categories/
Ответ:
json
[
  {
    "name": "Фильмы",
    "slug": "movies"
  },
  {
    "name": "Книги",
    "slug": "books"
  }
]

3. Создание произведения
Запрос:
POST /api/v1/titles/
json
{
  "name": "Интерстеллар",
  "year": 2014,
  "category": "movies",
  "genre": ["sci-fi"],
  "description": "Фантастический фильм о космосе."
}
Ответ:
json
{
  "id": 1,
  "name": "Интерстеллар",
  "year": 2014,
  "category": "movies",
  "genre": ["sci-fi"],
  "description": "Фантастический фильм о космосе."
}

Админка
Админ-панель доступна по адресу /admin/.
В админке зарегистрированы модели:
User (пользователи)
Category, Genre, Title (произведения)
Review, Comment (отзывы и комментарии)

Тестирование
Для запуска тестов используйте команду:
python manage.py test

Зависимости
Проект использует:
Django
Django REST framework
django-filter
djangorestframework-simplejwt
и другие...
Зависимости указаны в requirements.txt

Над проектом работали:
Дмитрий Радюк - https://github.com/Dzmitry-Radziuk 
Александр Лавер - https://github.com/XanterXAlexandr 
Михаил Яковенко - https://github.com/MikhailYakovenko