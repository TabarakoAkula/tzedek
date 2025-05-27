lint:
	poetry run black . --check --diff --color
	poetry run flake8 web --statistics --count --show-source
	poetry run flake8 telegram_bot --statistics --count --show-source

runweb:
	cd web && python manage.py runserver

celery:
	cd web && celery -A core worker -P threads -E

bot:
	python telegram_bot

devbot:
	poetry run python telegram_bot/autoreload.py

build:
	docker compose up --build

build_d:
	docker compose up -d --build
