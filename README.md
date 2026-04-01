# 🎬 YaMDb API

**YaMDb API** — это проект для сбора пользовательских отзывов о различных произведениях: фильмах, книгах, музыке и др.  
Реализован на базе **Django** и **Django REST Framework**, с использованием **JWT-аутентификации**.

---

## 📂 Структура проекта

```
api_yamdb/
├── api/                  # Основное приложение API
│   ├── common/           # Утилиты и валидаторы
│   ├── admin.py
│   ├── apps.py
│   ├── exceptions.py
│   ├── paginations.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── urls.py
│   ├── views.py
│   └── ...
│
├── api_yamdb/            # Настройки Django
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
│   └── ...
│
├── reviews/              # Отзывы и комментарии
├── titles/               # Произведения
│   └── management/commands/load_csv_data.py
├── users/                # Пользователи
│
├── static/data/          # CSV-данные
├── templates/            # HTML-шаблоны
│
├── manage.py
├── .env
├── db.sqlite3
└── requirements.txt
```

---

## 🚀 Установка и запуск

### 1. Клонирование репозитория
```bash
git clone https://github.com/Dzmitry-Radziuk/api_yamdb
cd api_yamdb
```

### 2. Виртуальное окружение
```bash
python -m venv venv
```

**Активация:**
- Windows:
```bash
venv\Scripts\activate
```
- Linux / macOS:
```bash
source venv/bin/activate
```

### 3. Установка зависимостей
```bash
pip install -r requirements.txt
```

### 4. Миграции
```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Создание суперпользователя (опционально)
```bash
python manage.py createsuperuser
```

---

## 📥 Загрузка данных

Импорт CSV-файлов:

```bash
python manage.py load_csv_data
```

Файлы должны находиться в папке:
```
static/data/
```

---

## ▶️ Запуск сервера

```bash
python manage.py runserver
```

📍 Адрес:
```
http://127.0.0.1:8000/
```

---

## 🔐 Аутентификация

### Регистрация
```http
POST /api/v1/auth/signup/
```

### Получение токена
```http
POST /api/v1/auth/token/
```

---

## 📚 Основные эндпоинты

### Категории
- `GET /api/v1/categories/` — список категорий
- `POST /api/v1/categories/` — создание (admin)

### Произведения
- `GET /api/v1/titles/` — список
- `POST /api/v1/titles/` — создание (admin)

Фильтрация:
- `category__slug`
- `genre__slug`
- `name`
- `year`

### Отзывы
- `GET /api/v1/titles/{title_id}/reviews/`
- `POST /api/v1/titles/{title_id}/reviews/`

### Комментарии
- `GET /api/v1/titles/{title_id}/reviews/{review_id}/comments/`
- `POST /api/v1/titles/{title_id}/reviews/{review_id}/comments/`

---

## 🧪 Примеры

### Регистрация
```json
{
  "username": "new_user",
  "email": "new_user@example.com"
}
```

### Категории
```json
[
  {
    "name": "Фильмы",
    "slug": "movies"
  }
]
```

### Создание произведения
```json
{
  "name": "Интерстеллар",
  "year": 2014,
  "category": "movies",
  "genre": ["sci-fi"],
  "description": "Фантастический фильм"
}
```

---

## ⚙️ Админ-панель

Доступ:
```
/admin/
```

Модели:
- Users
- Category / Genre / Title
- Review / Comment

---

## 🧪 Тестирование

```bash
python manage.py test
```

---

## 📦 Зависимости

- Django
- Django REST Framework
- django-filter
- djangorestframework-simplejwt

Полный список — в `requirements.txt`

---

## 👥 Авторы

- Дмитрий Радюк — https://github.com/Dzmitry-Radziuk  
- Александр Лавер — https://github.com/XanterXAlexandr  
- Михаил Яковенко — https://github.com/MikhailYakovenko  

---

## 📄 Документация

- `redoc.yaml`
- `/redoc/` в браузере

---

⭐ Проект учебный, но может служить хорошей основой для production API.
