#!/bin/sh
set -e
python wait_for.py
uv run python manage.py migrate --noinput
exec "$@"