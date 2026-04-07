"""Implementation for the ``init`` command."""

from __future__ import annotations

from pathlib import Path

from rich.panel import Panel
from rich.table import Table

from ..config import get_effective_config
from ..console import get_console
from ..scaffold import build_scaffold_options, create_scaffold


def run(project_name: str, *, directory: Path | None = None, force: bool = False) -> None:
    """Create a starter project scaffold and render a concise summary."""

    effective = get_effective_config()
    target_dir = directory or Path.cwd() / project_name
    options = build_scaffold_options(
        project_name,
        target_dir=target_dir,
        license_name=str(effective["scaffold_license"]),
        include_github_actions=bool(effective["scaffold_include_github_actions"]),
        include_pre_commit=bool(effective["scaffold_include_pre_commit"]),
    )
    written_files = create_scaffold(options, force=force)

    table = Table(show_header=False, box=None, padding=(0, 1))
    table.add_row("Project", options.project_name)
    table.add_row("Package", options.package_name)
    table.add_row("Command", options.command_name)
    table.add_row("Target", str(options.target_dir))
    table.add_row("Files written", str(len(written_files)))

    get_console().print(Panel.fit(table, title="Scaffold created", border_style="green"))
