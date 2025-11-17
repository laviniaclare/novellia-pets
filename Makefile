PYTHON ?= python3
VENV := .venv
PIP := $(VENV)/bin/pip
PY := $(VENV)/bin/python

.PHONY: help venv install run test clean

help:
	@echo "Makefile targets:"
	@echo "  make venv    - create virtualenv"
	@echo "  make install - install requirements into virtualenv"
	@echo "  make run     - run the app (creates venv & installs deps if needed)"
	@echo "  make dev     - run the app in development mode with auto-reload"
	@echo "  make test    - run pytest (creates venv & installs deps if needed)"

venv:
	@# create virtualenv if missing
	@test -d $(VENV) || $(PYTHON) -m venv $(VENV)
	@echo "Virtualenv ready at $(VENV)"

install: venv
	@$(PIP) install --upgrade pip
	@$(PIP) install -r requirements.txt

run: install
	@echo "Starting app..."
	@$(PY) run.py

dev: install
	@echo "Starting app in development mode (auto-reload)..."
	@# Use the flask CLI with the factory pattern: FLASK_APP=app:create_app
	@FLASK_APP=app:create_app FLASK_ENV=development $(VENV)/bin/flask run --host=127.0.0.1 --port=5000 --reload

test: install
	@$(PY) -m pytest -q

clean:
	@rm -rf $(VENV) .pytest_cache/__pycache__ .pytest_cache
