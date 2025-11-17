.PHONY: help \
        run migrate make-migrations create-superuser create-superuser-auto django-shell \
        format sort-imports lint test \
        run-docker migrate-docker make-migrations-docker create-superuser-docker \
        create-superuser-auto-docker django-shell-docker format-docker sort-imports-docker \
        lint-docker test-docker

help:
	@echo "Make команды:"
	@echo ""
	@echo " ЛОКАЛЬНО:"
	@echo "  make run                   - Запуск Django dev-сервера"
	@echo "  make migrate               - Применить миграции"
	@echo "  make make-migrations       - Создать миграции"
	@echo "  make create-superuser      - Создать суперпользователя"
	@echo "  make create-superuser-auto - Создать суперюзера admin/admin"
	@echo "  make django-shell          - Открыть Django shell"
	@echo "  make format                - Форматирование кода"
	@echo "  make sort-imports          - Сортировка импортов"
	@echo "  make lint                  - Линтер"
	@echo "  make test                  - Запуск pytest"
	@echo ""
	@echo " В DOCKER:"
	@echo "  make run-docker                   - Запуск сервера внутри контейнера"
	@echo "  make migrate-docker               - Миграции в контейнере"
	@echo "  make make-migrations-docker       - Создать миграции в контейнере"
	@echo "  make create-superuser-docker      - Создать суперпользователя в контейнере"
	@echo "  make create-superuser-auto-docker - Создать суперюзера admin/admin в контейнере"
	@echo "  make django-shell-docker          - Django shell в контейнере"
	@echo "  make format-docker                - Форматирование в контейнере"
	@echo "  make sort-imports-docker          - Сортировка импортов в контейнере"
	@echo "  make lint-docker                  - Линтер в контейнере"
	@echo "  make test-docker                  - Запуск pytest внутри docker-compose"

### ЛОКАЛЬНЫЕ КОМАНДЫ
run:
	uv run python manage.py runserver 0.0.0.0:8000

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


### DOCKER КОМАНДЫ
run-docker:
	docker compose exec app uv run python manage.py runserver 0.0.0.0:8000

migrate-docker:
	docker compose exec app uv run python manage.py migrate

make-migrations-docker:
	docker compose exec app uv run python manage.py makemigrations

create-superuser-docker:
	docker compose exec app uv run python manage.py createsuperuser

create-superuser-auto-docker:
	docker compose exec app uv run python manage.py shell -c "from django.contrib.auth import get_user_model; User=get_user_model(); User.objects.create_superuser('admin@example.com', 'admin') if not User.objects.filter(email='admin@example.com').exists() else None"

django-shell-docker:
	docker compose exec app uv run python manage.py shell

format-docker:
	docker compose exec app uv run ruff format .
	docker compose exec app uv run ruff check --fix .

sort-imports-docker:
	docker compose exec app uv run ruff check . --fix --select I

lint-docker:
	docker compose exec app uv run ruff check .

test-docker:
	docker compose run --rm app uv run pytest -q