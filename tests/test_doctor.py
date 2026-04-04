from __future__ import annotations

from typer.testing import CliRunner

from cmdforge.cli import app

runner = CliRunner()


def test_doctor_command_renders_expected_sections() -> None:
    result = runner.invoke(app, ["doctor"])
    assert result.exit_code == 0
    assert "Python" in result.stdout
    assert "Package" in result.stdout
    assert "Config" in result.stdout
