from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from cmdforge.cli import app
from cmdforge.config import get_config_path

runner = CliRunner()


def _set_xdg_env(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "cache"))


def test_config_show_works_without_existing_file(monkeypatch, tmp_path: Path) -> None:
    _set_xdg_env(monkeypatch, tmp_path)
    result = runner.invoke(app, ["config", "show"])
    assert result.exit_code == 0
    assert "color_system" in result.stdout
    assert "default" in result.stdout


def test_config_get_set_reset_flow(monkeypatch, tmp_path: Path) -> None:
    _set_xdg_env(monkeypatch, tmp_path)

    set_result = runner.invoke(app, ["config", "set", "scaffold_license", "Apache-2.0"])
    assert set_result.exit_code == 0
    assert get_config_path().exists()

    get_result = runner.invoke(app, ["config", "get", "scaffold_license"])
    assert get_result.exit_code == 0
    assert get_result.stdout.strip() == "Apache-2.0"

    reset_result = runner.invoke(app, ["config", "reset", "--yes"])
    assert reset_result.exit_code == 0
    assert not get_config_path().exists()

    post_reset_result = runner.invoke(app, ["config", "get", "scaffold_license"])
    assert post_reset_result.exit_code == 0
    assert post_reset_result.stdout.strip() == "MIT"


def test_invalid_config_key_returns_nonzero(monkeypatch, tmp_path: Path) -> None:
    _set_xdg_env(monkeypatch, tmp_path)
    result = runner.invoke(app, ["config", "get", "unknown_key"])
    assert result.exit_code == 2
    assert "Unknown config key" in result.stdout
