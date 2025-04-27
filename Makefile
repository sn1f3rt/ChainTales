CERTFILE ?= cert.pem
KEYFILE ?= key.pem

env:
	uv venv

install:
	uv sync --no-dev --extra prod

install-dev:
	uv sync --all-extras

export:
	uv export --format requirements-txt > requirements.txt

lint:
	cd src/apps/backend \
		&& mypy --config-file mypy.ini .

format:
	cd src/apps/backend \
		&& ruff check --select I --fix . && ruff format .

dev:
	cd src/apps/backend \
		&& PYTHONPATH=./ flask --app server:app run --host localhost --port 3000 --debug

prod:
	cd src/apps/backend \
		&& PYTHONPATH=./ gunicorn --bind 0.0.0.0:13139 server:app

prod-ssl:
	@if [ -z "$(word 1, $(filter-out $@,$(MAKECMDGOALS)))" ] || [ -z "$(word 2, $(filter-out $@,$(MAKECMDGOALS)))" ]; then \
		echo "Usage: make prod-ssl cert.pem key.pem"; \
		exit 1; \
	fi
	cd src/apps/backend \
		&& PYTHONPATH=./ gunicorn --bind 0.0.0.0:13139 server:app --certfile $(word 1, $(filter-out $@,$(MAKECMDGOALS))) --keyfile $(word 2, $(filter-out $@,$(MAKECMDGOALS)))

cmd:
	cd src/apps/backend \
		&& PYTHONPATH=./ flask --app server:app $(filter-out $@,$(MAKECMDGOALS))

reset-db:
	cd scripts && ./reset_db.sh $(filter-out $@,$(MAKECMDGOALS))

%:
	@:

.PHONY: env activate install install-dev export lint format dev prod prod-ssl cmd reset-db
.DEFAULT_GOAL := dev
