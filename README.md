# UAV Builder

## Requirements

* Docker

## Test Accounts

1. fuselage_user
2. tail_user
3. wing_user
4. assembly_user
5. avionics_user
6. admin

All accounts have the same password `baykar123456`

## Usage

Just run the command below and go to `http://localhost:8000`

`docker compose up -d`

## Running Tests

Just run below command while app is running:

`docker compose exec app poetry run python manage.py test`

## Linting

Inside av_builder folder

`black .`
`isort .`
`pylint *.py */*.py`
`flake8 .`
