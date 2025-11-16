.PHONY: help run migrate make-migrations create-superuser screate-uperuser-auto django-shell format sort-imports lint test

help:
	@echo "Make команды:"
	@echo "  make run                   - Запуск Django сервера разработки"
	@echo "  make migrate               - Применить миграции"
	@echo "  make make-migrations       - Создать миграции"
	@echo "  make create-superuser      - Создать суперпользователя"
	@echo "  make create-superuser-auto - Создать суперпользователя admin/admin"
	@echo "  make django-shell          - Открыть Django shell"
	@echo "  make format                - Форматирование кода (ruff format + auto-fix)"
	@echo "  make sort-imports          - Сортировка импортов"
	@echo "  make lint                  - Проверка кода линтером"
	@echo "  make test                  - Запуск тестов (pytest)"

run:
	uv run python manage.py runserver

migrate:
	uv run python manage.py migrate

make-migrations:
	uv run python manage.py makemigrations

create-superuser:
	uv run python manage.py createsuperuser

create-superuser-auto:
	uv run python manage.py shell -c "from django.contrib.auth import get_user_model; User=get_user_model(); User.objects.create_superuser('admin@example.com', 'admin') if not User.objects.filter(email='admin@example.com').exists() else None"

django-shell:
	uv run python manage.py shell

format:
	uv run ruff format .
	uv run ruff check --fix .

sort-imports:
	uv run ruff check . --fix --select I

lint:
	uv run ruff check .

test:
	uv run pytest -q