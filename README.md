# CMDforge

<div align="center">

<h1>CMDforge</h1>

<p>
  <strong>A polished Python CLI toolkit for building ergonomic, terminal-first applications.</strong>
</p>

<p>
  Build beautiful CLIs, inspect environments, manage config and cache safely, and generate clean starter projects with modern Python tooling.
</p>

<p>
  <a href="https://github.com/sureshreddy197/CMDforge/actions/workflows/ci.yml">
    <img src="https://github.com/sureshreddy197/CMDforge/actions/workflows/ci.yml/badge.svg" alt="CI">
  </a>
  <a href="LICENSE">
    <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License: MIT">
  </a>
  <img src="https://img.shields.io/badge/python-3.10%2B-blue.svg" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/CLI-Typer-7C3AED.svg" alt="Typer">
  <img src="https://img.shields.io/badge/output-Rich-111827.svg" alt="Rich">
  <img src="https://img.shields.io/badge/style-modern-success.svg" alt="Modern Python Project">
</p>

<p>
  <a href="#why-cmdforge">Why CMDforge</a> •
  <a href="#installation">Installation</a> •
  <a href="#quickstart">Quickstart</a> •
  <a href="#commands">Commands</a> •
  <a href="#configuration">Configuration</a> •
  <a href="#generated-scaffold">Generated Scaffold</a> •
  <a href="#development-setup">Development</a>
</p>

</div>

---

## Why CMDforge

CMDforge is both:

- a **useful developer utility**
- a **production-quality reference implementation**
- a **clean starter foundation** for terminal-first Python projects

It is intentionally small, practical, and maintainable, while still demonstrating the standards you would expect from a modern Python codebase.

### Highlights

- **Beautiful CLI UX** with Typer and thoughtful Rich output
- **Helpful diagnostics** via `cmdforge doctor`
- **Proper config storage** using platform-specific user config directories
- **Safe cache workflows** with clear inspection and cleanup commands
- **Real scaffold generation** for new CLI apps with tests and CI
- **Modern packaging and tooling** with `pyproject.toml`, Hatchling, Ruff, MyPy, pytest, and pre-commit
- **Readable structure** that is easy to learn from and extend

---

## At a glance

<table>
  <tr>
    <td width="33%" valign="top">
      <h3>🛠 Built for developers</h3>
      <p>Useful immediately as a CLI utility, while also serving as a high-quality project template.</p>
    </td>
    <td width="33%" valign="top">
      <h3>✨ Great terminal UX</h3>
      <p>Typer-based commands and polished Rich output make the interface clear and pleasant to use.</p>
    </td>
    <td width="33%" valign="top">
      <h3>📦 Modern by default</h3>
      <p>Comes with packaging, linting, formatting, typing, tests, and optional CI scaffolding.</p>
    </td>
  </tr>
</table>

---

## Installation

### Using `uv`

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

### Using `pip`

```bash
python -m pip install .
cmdforge --help
```

For editable development installs:

```bash
python -m pip install -e ".[dev]"
```

---

## Quickstart

Run a few commands to see what CMDforge offers:

```bash
cmdforge about
cmdforge version
cmdforge doctor
cmdforge config show
cmdforge init hello-cli
```

Example workflows:

```bash
cmdforge config set scaffold_license Apache-2.0
cmdforge config get scaffold_license
cmdforge cache info
cmdforge cache clear --yes
cmdforge init internal-tools --directory ./examples/internal-tools
```

### What it feels like

```bash
$ cmdforge doctor

Python Version     3.12.x
Platform           macOS-14.x-arm64
Executable         /Users/you/.local/bin/cmdforge
Package Version    0.x.x
Config Path        ~/.config/cmdforge/config.toml
Cache Path         ~/.cache/cmdforge
```

---

## Commands

### Core commands

| Command | Description |
|---|---|
| `cmdforge about` | Show project overview, version, summary, and repository URL |
| `cmdforge version` | Print the installed package version cleanly |
| `cmdforge doctor` | Inspect Python, platform, executable path, package version, config path, and cache path |
| `cmdforge init <project_name>` | Generate a complete Typer CLI starter project |

### Configuration commands

```bash
cmdforge config show
cmdforge config get <key>
cmdforge config set <key> <value>
cmdforge config reset [--yes]
```

### Cache commands

```bash
cmdforge cache info
cmdforge cache clear [--yes]
```

---

## Configuration

CMDforge stores user settings in a TOML file located in the platform-appropriate config directory provided by `platformdirs`.

### Config file location

- **Linux**: `~/.config/cmdforge/config.toml`
- **macOS**: `~/Library/Application Support/cmdforge/config.toml`
- **Windows**: `%APPDATA%\cmdforge\config.toml`

### Supported keys

- `color_system`
- `confirm_destructive_actions`
- `scaffold_license`
- `scaffold_include_github_actions`
- `scaffold_include_pre_commit`

### Examples

```bash
cmdforge config show
cmdforge config set color_system truecolor
cmdforge config set confirm_destructive_actions false
cmdforge config set scaffold_license BSD-3-Clause
cmdforge config reset --yes
```

### Supported scaffold licenses

- `MIT`
- `Apache-2.0`
- `BSD-3-Clause`

---

## Generated Scaffold

`cmdforge init` creates a clean starter repository with a practical baseline.

### Generated files

```text
your-project/
├── .editorconfig
├── .gitignore
├── LICENSE
├── README.md
├── pyproject.toml
├── src/
│   └── your_package/
│       ├── __main__.py
│       └── cli.py
└── tests/
```

### Optional extras

- `.pre-commit-config.yaml`
- `.github/workflows/ci.yml`

### What the scaffold gives you

- a **small, readable project layout**
- a **Typer-based CLI entrypoint**
- **tests** for the generated application
- **modern packaging defaults**
- optional **GitHub Actions CI**
- optional **pre-commit** setup

---

## Development Setup

### With `uv`

```bash
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"
pre-commit install
```

### With standard Python tooling

```bash
python -m pip install -e ".[dev]"
pre-commit install
```

---

## Quality Checks

CMDforge includes a modern quality toolchain for testing, linting, formatting, and type checking.

### Make targets

```bash
make test
make lint
make format-check
make typecheck
make check
```

### Equivalent direct commands

```bash
pytest
ruff check .
ruff format --check .
mypy src/cmdforge
```

---

## Project Structure

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

---

## Documentation

Additional documentation lives in `docs/`:

- [`docs/architecture.md`](docs/architecture.md)
- [`docs/development.md`](docs/development.md)

---

## Who this project is for

CMDforge is a strong fit if you want to:

- build a **Python CLI with excellent UX**
- study a **real-world project structure**
- bootstrap a new tool with **modern defaults**
- learn how Typer, Rich, pytest, Ruff, MyPy, and Hatchling work together
- keep your codebase **small, clean, and production-minded**

---

## Example use cases

- Internal developer tooling
- Team productivity CLIs
- Operational command suites
- Diagnostic utilities
- Project bootstrapping tools
- Small automation-focused terminal apps

---

## Roadmap

Ideas that fit the project well without bloating it:

- optional shell completion installation helpers
- export formats for diagnostics and config
- richer scaffold presets for libraries versus applications
- plugin hooks for additional internal developer tooling

---

## Contributing

Contributions are welcome.

Please read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a pull request.

---

## Security

If you discover a security issue, please follow the guidance in [SECURITY.md](SECURITY.md).

---

## License

CMDforge is released under the [MIT License](LICENSE).
