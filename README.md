# Тестовое задание

# Описание

Небольшое задание для работы с коллекцией мемов.

# Запуск проекта (локально)

1. Создать venv: `python -m venv venv` (linux)

2. Запустить docker-compose.dev.yml: `docker compose -f docker.compose.dev.yml up --build`

3. Запустить memes-service:

    * Добавить необходимые переменные окружения (DB_URI - адрес от БД, MINIO_SERVICE - адрес к API сервису S3)

    * Поставить необходимые зависимости: `cd memes-service/ && pip install -e .[dev]`

    * Применить миграции: `alembic upgrade head`

    * Запустить проект: `uvicorn --factory app.main:create_app`

4. Запустить minio-service:

    * Добавить необходимые переменные окружения (MINIO_ENDPOINT - адрес до MinIO, MINIO_ACCESS_KEY - access key или
      логин, MINIO_SECRET_KEY - secret key или пароль, MINIO_SECURE - состояние соединения, MINIO_BUCKET_NAME - название
      корзины, где будут сохранятся файлы)

    * Поставить необходимые зависимости: `cd minio-service/ && pip install -e .[dev]`

    * Запустить проект: `uvicorn --factory minio_app.main:create_app`

# Запуск проекта

1. Создать файл .env (пример параметров в .env.example)

2. Создать файл .env в memes-service (пример параметров в .env.example данного сервиса)

3. Создать файл .env в minio-service (пример параметров в .env.example данного сервиса)

4. Запустить проект: `make start`

5. Применить миграции: `make migrate`

# Доступные эндпоинты

* GET /memes - получение списка всех мемов

* GET /memes/{id} - получение конкретного мема по ID

* POST /memes - добавление нового мема (текст и изображение)

* PUT /memes/{id} - обновление существующего мема

* DELETE /memes/{id} - удаление мема
