PYTHON ?= python
PACKAGE := cmdforge

.PHONY: install dev-install format format-check lint typecheck test check build clean

install:
	$(PYTHON) -m pip install .

dev-install:
	$(PYTHON) -m pip install -e ".[dev]"

format:
	ruff format .

format-check:
	ruff format --check .

lint:
	ruff check .

typecheck:
	mypy src/$(PACKAGE)

test:
	pytest

check: lint format-check typecheck test

build:
	$(PYTHON) -m build

clean:
	rm -rf build dist .mypy_cache .pytest_cache .ruff_cache *.egg-info htmlcov .coverage coverage.xml
