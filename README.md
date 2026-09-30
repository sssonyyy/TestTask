# FastAPI + PostgreSQL in Docker

## Запуск

1. Создайте локальный файл с настройками:

   ```sh
   cp .env.example .env
   ```

2. При необходимости измените значения в `.env`. Пароль должен содержать только URL-safe символы, так как он используется для формирования строки подключения.

3. Соберите и запустите сервисы:

   ```sh
   docker compose up --build
   ```

API будет доступно по адресу <http://localhost:8000>, а Swagger UI — по адресу <http://localhost:8000/docs>.

PostgreSQL не публикует порт на хост: к нему может обращаться только API внутри Docker Compose. Данные PostgreSQL сохраняются в именованном томе `postgres_data`.

## Подключение вне Docker Compose

Перед запуском приложения укажите полную строку подключения в переменной `DATABASE_URL`, например:

```sh
export DATABASE_URL='postgresql+psycopg2://postgres:password@localhost:5432/TestDB'
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Данные

Файл `dump.sql` содержит схему и данные исходной базы, включая таблицу `respondents`. При первом запуске с пустым Docker volume PostgreSQL автоматически выполнит этот дамп. Поэтому после переноса всего проекта на другую машину достаточно выполнить `docker compose up --build`.

Если контейнеры уже запускались и volume `postgres_data` существует, PostgreSQL не применит дамп повторно, чтобы не перезаписать существующие данные. Для полного переинициализирования базы удалите том и запустите сервисы снова:

```sh
docker compose down --volumes
docker compose up --build
```

## Остановка

```sh
docker compose down
```

Команда выше сохраняет данные в томе. Чтобы удалить также данные PostgreSQL, выполните `docker compose down --volumes`.
