# CMDforge

[![CI](https://github.com/sureshreddy197/CMDforge/actions/workflows/ci.yml/badge.svg)](https://github.com/sureshreddy197/CMDforge/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

CMDforge is a polished Python CLI toolkit and reference implementation for building ergonomic command-line applications.
It ships as a useful developer utility, and it doubles as a production-quality example of how to structure, package, test, and document a modern terminal-first Python project.

## Why CMDforge?

- Beautiful Typer-based CLI with thoughtful Rich output
- Clear environment diagnostics via `cmdforge doctor`
- A small, robust TOML configuration system stored in the proper user config directory
- Cache inspection and cleanup commands with safe workflows
- A real scaffold generator that creates a clean starter CLI project with tests and CI
- Modern packaging with `pyproject.toml`, Hatchling, Ruff, MyPy, pytest, and pre-commit
- A maintainable module layout that is easy to learn from and extend

## Installation

### With `uv`

```bash
uv tool install .
cmdforge --help
```

For local development:

```bash
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"
```

### With `pip`

```bash
python -m pip install .
cmdforge --help
```

For editable development installs:

```bash
python -m pip install -e ".[dev]"
```

## Quickstart

```bash
cmdforge about
cmdforge version
cmdforge doctor
cmdforge config show
cmdforge init hello-cli
```

Example output-focused workflows:

```bash
cmdforge config set scaffold_license Apache-2.0
cmdforge config get scaffold_license
cmdforge cache info
cmdforge cache clear --yes
cmdforge init internal-tools --directory ./examples/internal-tools
```

## Commands

### Core commands

- `cmdforge about` — show project overview, version, summary, and repository URL
- `cmdforge version` — print the installed package version cleanly
- `cmdforge doctor` — inspect Python, platform, executable path, package version, config path, and cache path
- `cmdforge init <project_name>` — generate a complete Typer CLI starter project

### Configuration commands

- `cmdforge config show`
- `cmdforge config get <key>`
- `cmdforge config set <key> <value>`
- `cmdforge config reset [--yes]`

### Cache commands

- `cmdforge cache info`
- `cmdforge cache clear [--yes]`

## Configuration

CMDforge stores user settings in a TOML file inside the platform-appropriate config directory provided by `platformdirs`.
The file lives at:

- Linux: `~/.config/cmdforge/config.toml`
- macOS: `~/Library/Application Support/cmdforge/config.toml`
- Windows: `%APPDATA%\cmdforge\config.toml`

Supported keys:

- `color_system`
- `confirm_destructive_actions`
- `scaffold_license`
- `scaffold_include_github_actions`
- `scaffold_include_pre_commit`

Examples:

```bash
cmdforge config show
cmdforge config set color_system truecolor
cmdforge config set confirm_destructive_actions false
cmdforge config set scaffold_license BSD-3-Clause
cmdforge config reset --yes
```

Supported scaffold licenses are:

- `MIT`
- `Apache-2.0`
- `BSD-3-Clause`

## Generated scaffold

`cmdforge init` creates a clean starter repository with a practical baseline:

- `pyproject.toml`
- `README.md`
- `LICENSE`
- `.gitignore`
- `.editorconfig`
- optional `.pre-commit-config.yaml`
- optional `.github/workflows/ci.yml`
- `src/<package>/cli.py`
- `src/<package>/__main__.py`
- tests for the generated CLI

The generated project is intentionally small, readable, and ready to extend.

## Development setup

```bash
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"
pre-commit install
```

Or with standard tooling:

```bash
python -m pip install -e ".[dev]"
pre-commit install
```

## Testing, linting, formatting, and type checking

```bash
make test
make lint
make format-check
make typecheck
make check
```

Equivalent direct commands:

```bash
pytest
ruff check .
ruff format --check .
mypy src/cmdforge
```

## Project structure

```text
CMDforge/
├── .github/
├── docs/
├── src/
│   └── cmdforge/
│       ├── commands/
│       ├── cli.py
│       ├── config.py
│       ├── console.py
│       ├── doctor.py
│       ├── exceptions.py
│       ├── metadata.py
│       └── scaffold.py
└── tests/
```

## Documentation

Additional documentation lives in `docs/`:

- [`docs/architecture.md`](docs/architecture.md)
- [`docs/development.md`](docs/development.md)

## Contributing

Contributions are welcome. Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

## Security

If you discover a security issue, please follow the guidance in [SECURITY.md](SECURITY.md).

## Roadmap

Ideas that fit the project well without bloating it:

- optional shell completion installation helpers
- export formats for diagnostics and config
- richer scaffold presets for libraries versus applications
- plugin hooks for additional internal developer tooling

## License

CMDforge is released under the [MIT License](LICENSE).
