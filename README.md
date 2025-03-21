# YaMDb API

Проект **YaMDb** собирает отзывы пользователей о различных произведениях (фильмах, книгах, песнях и т.д.). API реализовано с использованием Django и Django REST framework, а аутентификация – через JWT.

## Структура проекта

api_yamdb/ ├── api_yamdb/ # Корневая директория проекта Django │ ├── init.py │ ├── settings.py # Настройки проекта │ ├── urls.py # Основные маршруты │ ├── wsgi.py │ └── manage.py ├── reviews/ # Приложение для отзывов и комментариев │ ├── migrations/ │ ├── management/ │ │ ├── init.py │ │ └── commands/ │ │ ├── init.py │ │ └── load_csv_data.py # Команда для импорта CSV │ ├── models.py # Модели: Review, Comment │ ├── serializers.py │ ├── views.py │ └── ... ├── titles/ # Приложение для произведений │ ├── migrations/ │ ├── models.py # Модели: Title, Category, Genre │ ├── serializers.py │ ├── views.py │ └── ... ├── users/ # Приложение для пользователей │ ├── migrations/ │ ├── models.py # Модель User (или кастомная модель) │ ├── serializers.py │ ├── views.py │ └── ... ├── static/ │ └── data/ # Директория с CSV-файлами │ ├── category.csv │ ├── genre.csv │ ├── titles.csv │ ├── users.csv │ ├── review.csv │ └── comments.csv ├── api/ # Единая админка и общие файлы (по необходимости) │ └── admin.py # Админка для всех моделей ├── requirements.txt # Список зависимостей └── README.md # Этот файл

## Установка

1. **Клонируйте репозиторий:**
   git clone <URL вашего репозитория>
   cd api_yamdb

**Создайте и активируйте виртуальное окружение:**
  python -m venv .venv
# Windows:
  .venv\Scripts\activate
# Linux/macOS:
  source .venv/bin/activate

**Установите зависимости:**
  pip install -r requirements.txt

**Примените миграции:**
  python manage.py makemigrations
  python manage.py migrate

**Создайте суперпользователя (опционально):**
  python manage.py createsuperuser

**Загрузка данных из CSV**
  Для массового импорта данных из CSV-файлов используется команда load_csv_data. CSV-файлы должны находиться в папке static/data/.

**Запустите импорт командой:**

  python manage.py load_csv_data
  После выполнения вы увидите сообщения об успешной загрузке записей в соответствующие модели.

**Запуск сервера**
  Чтобы запустить сервер разработки, выполните:

  python manage.py runserver
  Сервер будет доступен по адресу http://127.0.0.1:8000/

**API Эндпоинты**
  API начинается с /api/v1/. Некоторые основные эндпоинты:

  Auth:

  POST /api/v1/auth/signup/ – регистрация пользователя (отправка email и username).
  POST /api/v1/auth/token/ – получение JWT-токена (по username и confirmation_code).
  Категории:

  GET /api/v1/categories/ – получение списка категорий (без токена).
  POST /api/v1/categories/ – создание категории (только для администраторов).
  DELETE /api/v1/categories/{slug}/ – удаление категории (только для администраторов).
  Жанры:

  GET /api/v1/genres/ – получение списка жанров (без токена).
  POST /api/v1/genres/ – создание жанра (только для администраторов).
  DELETE /api/v1/genres/{slug}/ – удаление жанра (только для администраторов).
  Произведения:

  GET /api/v1/titles/ – получение списка произведений (без токена), поддерживается фильтрация по category__slug, genre__slug, name и year.
  POST /api/v1/titles/ – добавление произведения (только для администраторов). При добавлении нельзя указывать год выпуска больше текущего.
  GET /api/v1/titles/{title_id}/ – получение информации о произведении (без токена).
  PATCH /api/v1/titles/{title_id}/ – частичное обновление произведения (только для администраторов).
  DELETE /api/v1/titles/{title_id}/ – удаление произведения (только для администраторов).
  Отзывы и комментарии:

  GET /api/v1/titles/{title_id}/reviews/ – получение отзывов для произведения (без токена).
  POST /api/v1/titles/{title_id}/reviews/ – создание отзыва (только для аутентифицированных пользователей, один отзыв на произведение).
  GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/ – получение комментариев к отзыву (без токена).
  POST /api/v1/titles/{title_id}/reviews/{review_id}/comments/ – создание комментария (только для аутентифицированных пользователей).
  Полное описание эндпоинтов находится в файле redoc.yaml.

**Админка**
  Админ-панель доступна по адресу /admin/.
  В админке зарегистрированы модели:

  User (пользователи)
  Category, Genre, Title (произведения)
  Review, Comment (отзывы и комментарии)

**Тестирование**
  Для запуска тестов используйте команду:
  python manage.py test

**Зависимости**
  Django
  Django REST framework
  django-filter
  djangorestframework-simplejwt
  и другие зависимости, указанные в requirements.txt

**Над проектом работали:**
  Дмитрий Радюк   - https://github.com/Dzmitry-Radziuk
  Александр Лавер - https://github.com/XanterXAlexandr
  Михаил Яковенко - https://github.com/MikhailYakovenko
