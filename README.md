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

