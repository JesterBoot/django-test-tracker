# django-test-tracker

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


## Локальная разработка

### 1. Установка зависимостей

Проект использует менеджер пакетов `uv`:

```bash
uv sync
```

### 2. Настройка окружения

Создайте файл `.env`:

```bash
cp .env.example .env
```

Для локальной разработки значения из `.env.example` подходят по умолчанию.

### 3. Поднять базу данных

#### Вариант A: Локальная установка PostgreSQL  
Убедитесь, что параметры подключения в `.env` соответствуют вашей локальной базе данных.

#### Вариант B: Поднять PostgreSQL через Docker Compose

```bash
docker compose up -d
```

База данных будет доступна на `localhost:5432`.

### 4. Применение миграций

```bash
make migrate
```

### 5. Создать суперпользователя

#### Вариант A: вручную

```bash
make create-superuser
```

#### Вариант B: автоматически (admin/admin)

```bash
make create-superuser-auto
```

Будет создан суперпользователь:

- username: `admin`  
- email: `admin@example.com`  
- password: `admin`

### 6. Запуск сервера разработки

```bash
make run
```

Сервер будет доступен по адресу:

```
http://127.0.0.1:8000
```
