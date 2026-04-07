"""Implementation for the ``doctor`` command."""

from __future__ import annotations

from rich.panel import Panel
from rich.table import Table

from ..console import get_console
from ..doctor import collect_diagnostics
from ..metadata import APP_NAME


def run() -> None:
    """Render an environment diagnostics report."""

    report = collect_diagnostics()
    table = Table(show_header=True, header_style="bold cyan", expand=True)
    table.add_column("Check", ratio=1)
    table.add_column("Value", ratio=3)
    table.add_row("Python version", report.python_version)
    table.add_row("Implementation", report.python_implementation)
    table.add_row("Platform", report.platform_name)
    table.add_row("Executable", str(report.executable_path))
    table.add_row("Package version", report.package_version)
    table.add_row("Config directory", str(report.config_directory))
    table.add_row("Cache directory", str(report.cache_directory))
    table.add_row("Config file", str(report.config_file))
    table.add_row("Config file exists", "yes" if report.config_file_exists else "no")
    table.add_row("Working directory", str(report.current_working_directory))

    get_console().print(Panel.fit(table, title=f"{APP_NAME} doctor", border_style="cyan"))
