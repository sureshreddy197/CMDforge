from __future__ import annotations

from typer.testing import CliRunner

from cmdforge.cli import app
from cmdforge.metadata import REPOSITORY_URL, VERSION

runner = CliRunner()


def test_help_works() -> None:
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert "ergonomic" in result.stdout
    assert "command-line apps" in result.stdout
    assert "cmdforge init hello-cli" in result.stdout


def test_version_command_outputs_clean_version() -> None:
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert result.stdout.strip() == VERSION


def test_about_command_displays_project_metadata() -> None:
    result = runner.invoke(app, ["about"])
    assert result.exit_code == 0
    assert "CMDforge" in result.stdout
    assert REPOSITORY_URL in result.stdout
