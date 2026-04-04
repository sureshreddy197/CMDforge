# Development Guide

## Environment setup

### With `uv`

```bash
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"
pre-commit install
```

### With `pip`

```bash
python -m pip install -e ".[dev]"
pre-commit install
```

## Day-to-day workflow

A typical local cycle looks like this:

```bash
ruff format .
ruff check .
mypy src/cmdforge
pytest
```

Or use the Makefile wrappers:

```bash
make format
make lint
make typecheck
make test
make check
```

## Working on commands

When adding or changing a command:

1. put domain logic in an existing support module or a new focused module
2. keep the command function in `cli.py` thin
3. add user-facing rendering in `commands/`
4. add or update tests that exercise the CLI through `CliRunner`

This keeps behavior easy to trace and avoids giant entrypoint files.

## Working on configuration

Configuration lives in `src/cmdforge/config.py`.
When adding a new key:

1. add a `ConfigField` entry with a default, description, parser, and optional allowed values
2. document the key in `README.md`
3. add tests for reading, setting, and validation
4. use the value from commands only where it adds clear user value

## Working on the scaffold generator

The scaffold is rendered by explicit string templates in `src/cmdforge/scaffold.py`.
That means changes should be made carefully and tested by inspecting generated output.

When modifying scaffold behavior:

- keep file contents coherent with the main repository quality bar
- avoid adding dependencies that only benefit the generated starter marginally
- update `tests/test_scaffold.py`

## Release workflow

A practical lightweight release flow:

1. update `CHANGELOG.md`
2. bump the version in `src/cmdforge/metadata.py` and `pyproject.toml`
3. run `make check`
4. build the package with `make build`
5. tag and push the release in GitHub

## CI behavior

The GitHub Actions workflow installs the project in editable mode and runs:

- Ruff linting
- Ruff formatting check
- MyPy type checks
- pytest

Keep CI realistic and fast. Prefer stable tooling over clever pipeline tricks.
