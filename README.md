# Habit Tracker API

Backend-сервис для трекинга привычек с напоминаниями через Telegram.

Проект реализован на **Django REST Framework**, с поддержкой:
- JWT-аутентификации
- пользовательских привычек
- публичных привычек
- валидаций по ТЗ
- фоновых задач (Celery + Redis)
- Telegram-уведомлений
- автоматических тестов

---

## Стек технологий

- Python 3.12
- Django 5 / Django REST Framework
- PostgreSQL
- JWT (SimpleJWT)
- Celery
- Redis
- Telegram Bot API
- unittest (DRF APITestCase)
- Coverage

---

## Функциональность

### Пользователи
- Регистрация пользователя
- Авторизация (JWT access / refresh)
- Привязка Telegram `chat_id` к пользователю

### Привычки
- CRUD привычек (только для владельца)
- Просмотр только своих привычек
- Публичный список привычек (доступен без авторизации)
- Пагинация (5 привычек на страницу)

### Валидации (согласно ТЗ)
- Нельзя одновременно указывать `reward` и `related_habit`
- `duration_seconds` ≤ 120 секунд
- `periodicity` — от 1 до 7 дней
- `related_habit` может быть только с `is_pleasant=True`
- Если `is_pleasant=True` — нельзя указывать `reward` и `related_habit`

### Напоминания
- Отправка напоминаний о привычках через Telegram
- Фоновые задачи реализованы через Celery

---

## Установка и запуск

### 1. Клонировать репозиторий

```bash
git clone <repo_url>
cd habit-tracker
```

### 2) Установка зависимостей
```bash
poetry install
```

### 3) Создание файла .env

Создайте файл `.env` в корне проекта (рядом с `manage.py`).

В качестве основы можно использовать файл `.env.example`.

#### Пример `.env`:

```env
# Django
DEBUG=True
SECRET_KEY=your_secret_key
ALLOWED_HOSTS=127.0.0.1,localhost
TIME_ZONE=Europe/Moscow

# Database (PostgreSQL)
DB_NAME=habit_tracker
DB_USER=habit_user
DB_PASSWORD=habit_password
DB_HOST=localhost
DB_PORT=5432

# CORS (frontend)
CORS_ALLOW_ALL_ORIGINS=True

# Telegram
TELEGRAM_BOT_TOKEN=your_telegram_bot_token

# Celery / Redis
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

**Важно:** файл `.env` содержит конфиденциальные данные, не должен добавляться в репозиторий 
и обязательно должен быть указан в `.gitignore`.

### 4) Применение миграций
```bash
poetry run python manage.py migrate
```

### 5) Запуск сервера
```bash
poetry run python manage.py runserver
```

После запуска сервера:

- **API** доступен по адресу:  
  http://127.0.0.1:8000/

- **Документация API (Swagger)**:  
  http://127.0.0.1:8000/api/docs/

## Celery и Redis

Для работы системы напоминаний требуется **Redis**.

### Запуск Redis (пример)

```bash
redis-server
```

### Запуск Celery worker

```bash
poetry run celery -A config worker -l info
```

### (Опционально) Запуск Celery beat

Используется для выполнения периодических задач.

```bash
poetry run celery -A config beat -l info
```

## Тестирование

В проекте используются стандартные инструменты тестирования **Django REST Framework** (`APITestCase`).

### Запуск тестов

```bash
poetry run python manage.py test
```

### Проверка покрытия кода

Запуск тестов с анализом покрытия:

```bash
poetry run coverage run manage.py test
poetry run coverage report -m
```

Текущее покрытие кода на момент написания: **~98%**.

## Авторизация

Для доступа к защищённым эндпоинтам используется **JWT-аутентификация**.

### Регистрация пользователя

```http
POST /api/auth/register/
```

### Получение токена

```http
POST /api/auth/token/
```

### Использование токена

Токен передаётся в заголовке каждого авторизованного запроса:

```http
Authorization: Bearer <access_token>
```

## Автор

**Backend-разработка** — Olga Noskova
