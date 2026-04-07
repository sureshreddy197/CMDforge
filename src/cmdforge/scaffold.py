"""Project scaffold generation for the ``init`` command."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from .config import SUPPORTED_LICENSES
from .exceptions import ScaffoldError

MIT_LICENSE = """MIT License

Copyright (c) 2026 Suresh Reddy

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the \"Software\"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED \"AS IS\", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

APACHE_LICENSE = """Apache License
Version 2.0, January 2004
http://www.apache.org/licenses/

Copyright 2026 Suresh Reddy

Licensed under the Apache License, Version 2.0 (the \"License\");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an \"AS IS\" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

BSD_3_LICENSE = """BSD 3-Clause License

Copyright (c) 2026, Suresh Reddy
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors
   may be used to endorse or promote products derived from this software
   without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS \"AS IS\"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""


@dataclass(frozen=True)
class ScaffoldOptions:
    """Normalized scaffold parameters."""

    project_name: str
    package_name: str
    distribution_name: str
    command_name: str
    target_dir: Path
    license_name: str
    include_github_actions: bool
    include_pre_commit: bool


LICENSE_TEMPLATES = {
    "MIT": MIT_LICENSE,
    "Apache-2.0": APACHE_LICENSE,
    "BSD-3-Clause": BSD_3_LICENSE,
}


def normalize_project_name(project_name: str) -> str:
    """Validate and normalize the user-facing project name."""

    name = project_name.strip()
    if not name:
        raise ScaffoldError("Project name cannot be empty.")
    return name


def _normalize_package_name(project_name: str) -> str:
    candidate = re.sub(r"[^A-Za-z0-9]+", "_", project_name.strip().lower()).strip("_")
    if not candidate:
        raise ScaffoldError("Could not derive a valid Python package name from the project name.")
    if candidate[0].isdigit():
        candidate = f"app_{candidate}"
    return candidate


def _normalize_distribution_name(project_name: str) -> str:
    candidate = re.sub(r"[^A-Za-z0-9]+", "-", project_name.strip().lower()).strip("-")
    if not candidate:
        raise ScaffoldError("Could not derive a valid distribution name from the project name.")
    if candidate[0].isdigit():
        candidate = f"app-{candidate}"
    return candidate


def build_scaffold_options(
    project_name: str,
    *,
    target_dir: Path,
    license_name: str,
    include_github_actions: bool,
    include_pre_commit: bool,
) -> ScaffoldOptions:
    """Construct validated scaffold options for filesystem rendering."""

    name = normalize_project_name(project_name)
    if license_name not in SUPPORTED_LICENSES:
        supported = ", ".join(sorted(SUPPORTED_LICENSES))
        raise ScaffoldError(
            f"Unsupported scaffold license '{license_name}'. Supported values: {supported}."
        )

    distribution_name = _normalize_distribution_name(name)
    return ScaffoldOptions(
        project_name=name,
        package_name=_normalize_package_name(name),
        distribution_name=distribution_name,
        command_name=distribution_name,
        target_dir=target_dir,
        license_name=license_name,
        include_github_actions=include_github_actions,
        include_pre_commit=include_pre_commit,
    )


def create_scaffold(options: ScaffoldOptions, *, force: bool = False) -> list[Path]:
    """Create a fully populated starter repository and return written files."""

    target = options.target_dir
    if target.exists() and any(target.iterdir()) and not force:
        raise ScaffoldError(
            f"Target directory '{target}' already exists and is not empty. "
            "Use --force to overwrite files."
        )
    target.mkdir(parents=True, exist_ok=True)

    files = _render_files(options)
    written: list[Path] = []
    for relative_path, content in files.items():
        destination = target / relative_path
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8")
        written.append(destination)
    return written


def _render_files(options: ScaffoldOptions) -> dict[Path, str]:
    files: dict[Path, str] = {
        Path(".editorconfig"): _scaffold_editorconfig(),
        Path(".gitignore"): _scaffold_gitignore(),
        Path("LICENSE"): _scaffold_license(options),
        Path("README.md"): _scaffold_readme(options),
        Path("pyproject.toml"): _scaffold_pyproject(options),
        Path(f"src/{options.package_name}/__init__.py"): (
            "__all__ = [\"__version__\"]\n__version__ = \"0.1.0\"\n"
        ),
        Path(f"src/{options.package_name}/__main__.py"): _scaffold_main(),
        Path(f"src/{options.package_name}/cli.py"): _scaffold_cli(options),
        Path("tests/test_cli.py"): _scaffold_test(options),
    }
    if options.include_pre_commit:
        files[Path(".pre-commit-config.yaml")] = _scaffold_pre_commit()
    if options.include_github_actions:
        files[Path(".github/workflows/ci.yml")] = _scaffold_ci()
    return files


def _scaffold_editorconfig() -> str:
    return """root = true

[*]
charset = utf-8
end_of_line = lf
indent_style = space
indent_size = 4
insert_final_newline = true
trim_trailing_whitespace = true

[*.md]
trim_trailing_whitespace = false
"""


def _scaffold_gitignore() -> str:
    return """__pycache__/
*.py[cod]
.venv/
.mypy_cache/
.pytest_cache/
.ruff_cache/
dist/
build/
*.egg-info/
.DS_Store
"""


def _scaffold_license(options: ScaffoldOptions) -> str:
    template = LICENSE_TEMPLATES[options.license_name]
    return template.format(holder=options.project_name)


def _scaffold_readme(options: ScaffoldOptions) -> str:
    return f"""# {options.project_name}

A clean, minimal Typer-based CLI starter generated by CMDforge.

## Features

- Modern `pyproject.toml` packaging with a `src/` layout
- Rich help and friendly terminal output
- A tiny but complete Typer application
- Pytest coverage for the main CLI behavior
- Ruff formatting and linting
- Optional GitHub Actions CI and pre-commit hooks

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -e .[dev]
{options.command_name} --help
```

## Available commands

```bash
{options.command_name} --help
{options.command_name} hello --name Developer
{options.command_name} version
```

## Development

```bash
python -m pip install -e .[dev]
ruff check .
ruff format --check .
pytest
```

## License

This project is licensed under the {options.license_name} license. See `LICENSE`.
"""


def _scaffold_pyproject(options: ScaffoldOptions) -> str:
    return f"""[build-system]
requires = [\"hatchling>=1.25.0\"]
build-backend = \"hatchling.build\"

[project]
name = \"{options.distribution_name}\"
version = \"0.1.0\"
description = \"A Typer CLI starter generated by CMDforge.\"
readme = \"README.md\"
license = {{ file = \"LICENSE\" }}
requires-python = \">=3.10\"
dependencies = [
  \"rich>=13.7.0,<15.0.0\",
  \"typer>=0.12.3,<1.0.0\",
]

[project.optional-dependencies]
dev = [
  \"pytest>=8.3.2\",
  \"ruff>=0.6.9\",
]

[project.scripts]
{options.command_name} = \"{options.package_name}.cli:main\"

[tool.hatch.build.targets.wheel]
packages = [\"src/{options.package_name}\"]

[tool.ruff]
line-length = 100
target-version = \"py310\"

[tool.pytest.ini_options]
addopts = \"-ra\"
testpaths = [\"tests\"]
"""


def _scaffold_main() -> str:
    return """from .cli import main


if __name__ == \"__main__\":
    main()
"""


def _scaffold_cli(options: ScaffoldOptions) -> str:
    return f'''from __future__ import annotations

import typer
from rich.console import Console
from rich.panel import Panel

from . import __version__

app = typer.Typer(
    add_completion=False,
    no_args_is_help=True,
    help="A clean Typer CLI starter generated by CMDforge.",
    rich_markup_mode="rich",
)
console = Console()


@app.command()
def hello(name: str = typer.Option("Developer", "--name", help="Name to greet.")) -> None:
    """Print a friendly greeting."""

    console.print(
        Panel.fit(f"Hello, [bold cyan]{{name}}[/bold cyan]!", title="{options.project_name}")
    )


@app.command()
def version() -> None:
    """Print the installed package version."""

    console.print(__version__)


def main() -> None:
    app(prog_name="{options.command_name}")
'''


def _scaffold_test(options: ScaffoldOptions) -> str:
    return f"""from __future__ import annotations

from typer.testing import CliRunner

from {options.package_name}.cli import app

runner = CliRunner()


def test_help_works() -> None:
    result = runner.invoke(app, [\"--help\"])
    assert result.exit_code == 0
    assert \"A clean Typer CLI starter generated by CMDforge.\" in result.stdout


def test_version_command() -> None:
    result = runner.invoke(app, [\"version\"])
    assert result.exit_code == 0
    assert result.stdout.strip() == \"0.1.0\"
"""


def _scaffold_pre_commit() -> str:
    return """repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: end-of-file-fixer
      - id: trailing-whitespace
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.11.8
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
"""


def _scaffold_ci() -> str:
    return """name: CI

on:
  push:
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        python-version: [\"3.10\", \"3.11\", \"3.12\"]

    steps:
      - name: Check out repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install project
        run: |
          python -m pip install --upgrade pip
          python -m pip install -e .[dev]

      - name: Lint
        run: ruff check .

      - name: Test
        run: pytest
"""
