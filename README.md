## django-test-tracker
- Django 5 + DRF backend для управления задачами (создание, назначение исполнителя, изменение статуса, комментарии).
- JWT-аутентификация через `djangorestframework-simplejwt`; документация API через `drf-spectacular` (Swagger/Redoc).
- Приложения: `users` (регистрация, вход, refresh, выбор исполнителей), `workflows` (tasks + comments).
- Прав доступа:
  - Задачи: редактировать может только создатель или назначенный исполнитель; удалять — только создатель.
  - Комментарии: редактировать/удалять может только автор.
- Для продакшна: нужно внести изменения для WSGI/ASGI сервера (gunicorn/uvicorn+daphne).

## Троттлинг и кеш
- Redis используется как кеш и для DRF throttling. См. `core/throttling.py`:
  - LoginRateThrottle — по IP (scope `login`, 5/мин по умолчанию).
  - RefreshTokenRateThrottle — по `user_id` из refresh-токена, отпускает запрос, если токен битый.
- Базовые лимиты: `anon: 20/min`, `user: 100/min`; переопределяются в `REST_FRAMEWORK["DEFAULT_THROTTLE_RATES"]`.
- Для локальных тестов без Redis можно временно переключить кеш на LocMem в отдельном settings-файле или поднимать Redis в compose.

## Environment Variables

Используется `.env` в корне.  
Шаблон и пример значений, можно использовать значения для локальной разработки - `.env.example`.

### Переменные окружения
| Переменная                  | Описание                                                              |
|-----------------------------|-----------------------------------------------------------------------|
| `ENV`                       | Окружение приложения (`development`, `test`, `staging`, `production`) |
| `SECRET_KEY`                | Секретный ключ Django (обязательно заменить в проде)                  |
| `ALLOWED_HOSTS`             | Список разрешённых доменов через запятую                              |
| `POSTGRES_DB`               | Имя базы данных                                                       |
| `POSTGRES_USER`             | Пользователь базы                                                     |
| `POSTGRES_PASSWORD`         | Пароль пользователя                                                   |
| `POSTGRES_HOST`             | Хост PostgreSQL                                                       |
| `POSTGRES_PORT`             | Порт PostgreSQL                                                       |
| `JWT_ACCESS_LIFETIME_MIN`   | Срок жизни access-токена в минутах                                    |
| `JWT_REFRESH_LIFETIME_DAYS` | Срок жизни refresh-токена в днях                                      |
| `API_TITLE`                 | Название API для документации                                         |
| `API_VERSION`               | Версия API                                                            |
| `REDIS_HOST`                | Redis хост                                                            |
| `REDIS_PORT`                | Redis порт                                                            |
| `REDIS_DB`                  | Redis индекс бд                                                       |


## Запуск

### Docker:
1. Скопировать `.env.example` → `.env` и для docker указать `POSTGRES_HOST=db`, `REDIS_HOST=redis`.
2. Поднять стек (app + Postgres + Redis):
   ```bash
   docker compose up --build -d
   ```
3. Миграции и при необходимости создать суперпользователя:
   ```bash
   docker compose exec app uv run python manage.py migrate
   docker compose exec app uv run python manage.py createsuperuser  # опционально
   ```
4. Приложение: `http://127.0.0.1:8000`. 
5. Тесты: `docker compose exec app uv run pytest -q`.

### Локально (без Docker):
1. Установить зависимости:
   ```bash
   uv sync
   ```
2. Настроить окружение:
   ```bash
   cp .env.example .env
   ```
3. Поднять Postgres/Redis локально или через `docker compose up -d` (можно без сервиса `app`).
4. Миграции:
   ```bash
   make migrate
   ```
5. Суперпользователя (опционально):
   ```bash
   make create-superuser  # или make create-superuser-auto
   ```
6. Запуск сервер разработки:
   ```bash
   make run
   ```
   Доступен: `http://127.0.0.1:8000`.
