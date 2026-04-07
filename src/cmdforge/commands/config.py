"""Implementation for the ``config`` command group."""

from __future__ import annotations

from rich.table import Table

from ..config import (
    describe_config,
    get_config_path,
    get_config_value,
    reset_config,
    set_config_value,
)
from ..console import get_console, print_success, print_warning


def show() -> None:
    """Render the effective configuration in a Rich table."""

    table = Table(show_header=True, header_style="bold cyan", expand=True)
    table.add_column("Key", ratio=2)
    table.add_column("Value", ratio=2)
    table.add_column("Source", ratio=1)
    table.add_column("Description", ratio=3)

    for entry in describe_config():
        table.add_row(entry.key, str(entry.value), entry.source, entry.description)

    get_console().print(table)
    get_console().print(f"\n[dim]Config file:[/dim] {get_config_path()}")


def get_value(key: str) -> str:
    """Return a single configuration value as a plain string."""

    return str(get_config_value(key))


def set_value(key: str, value: str) -> None:
    """Persist a configuration value and show a confirmation message."""

    stored = set_config_value(key, value)
    print_success(f"Stored '{key}' = {stored} in {get_config_path()}.")


def reset() -> None:
    """Reset the configuration to defaults and report the result."""

    removed = reset_config()
    if removed:
        print_success("Configuration reset to defaults.")
    else:
        print_warning("No config file was present. Defaults are already active.")
