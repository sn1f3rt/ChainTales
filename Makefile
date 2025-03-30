env:
	uv venv

activate:
	source .venv/bin/activate

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
		&& PYTHONPATH=./ gunicorn --bind 0.0.0.0:3000 server:app

prod-ssl:
	cd src/apps/backend \
		&& PYTHONPATH=./ gunicorn --bind 0.0.0.0:3000 server:app $(filter-out $@,$(MAKECMDGOALS))

cmd:
	cd src/apps/backend \
		&& PYTHONPATH=./ flask --app server:app $(filter-out $@,$(MAKECMDGOALS))

%:
	@:

.PHONY: env activate install install-dev export lint format dev prod prod-ssl cmd
.DEFAULT_GOAL := debug
