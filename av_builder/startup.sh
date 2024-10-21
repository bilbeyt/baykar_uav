#!/usr/bin/env sh

cd /src
poetry run python manage.py migrate
poetry run python manage.py loaddata data.json
poetry run python manage.py runserver 0.0.0.0:8000