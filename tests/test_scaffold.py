from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from cmdforge.cli import app

runner = CliRunner()


def _set_xdg_env(monkeypatch, tmp_path: Path) -> None:
    monkeypatch.setenv("HOME", str(tmp_path))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "cache"))


def test_init_creates_expected_scaffold(monkeypatch, tmp_path: Path) -> None:
    _set_xdg_env(monkeypatch, tmp_path)

    project_dir = tmp_path / "demo-tool"
    result = runner.invoke(app, ["init", "demo-tool", "--directory", str(project_dir)])
    assert result.exit_code == 0

    expected_files = [
        project_dir / "pyproject.toml",
        project_dir / "README.md",
        project_dir / ".gitignore",
        project_dir / ".editorconfig",
        project_dir / "LICENSE",
        project_dir / ".github/workflows/ci.yml",
        project_dir / "src/demo_tool/cli.py",
        project_dir / "src/demo_tool/__main__.py",
        project_dir / "tests/test_cli.py",
    ]
    for expected in expected_files:
        assert expected.exists(), f"Missing scaffold file: {expected}"

    pyproject_contents = (project_dir / "pyproject.toml").read_text(encoding="utf-8")
    assert 'name = "demo-tool"' in pyproject_contents
    assert 'demo-tool = "demo_tool.cli:main"' in pyproject_contents


def test_init_refuses_to_overwrite_non_empty_directory(monkeypatch, tmp_path: Path) -> None:
    _set_xdg_env(monkeypatch, tmp_path)

    project_dir = tmp_path / "existing"
    project_dir.mkdir()
    (project_dir / "keep.txt").write_text("do not remove", encoding="utf-8")

    result = runner.invoke(app, ["init", "existing", "--directory", str(project_dir)])
    assert result.exit_code == 2
    assert "already exists and is not empty" in result.stdout
