"""Implementation for the ``about`` command."""

from __future__ import annotations

from rich.table import Table

from ..console import branded_panel, get_console
from ..metadata import APP_NAME, REPOSITORY_URL, SUMMARY, TAGLINE, VERSION


def run() -> None:
    """Render a concise project overview."""

    console = get_console()
    table = Table.grid(padding=(0, 2))
    table.add_row("[bold]Version[/bold]", VERSION)
    table.add_row("[bold]Package[/bold]", "cmdforge")
    table.add_row("[bold]CLI[/bold]", "cmdforge")
    table.add_row("[bold]Repository[/bold]", REPOSITORY_URL)
    table.add_row("[bold]Summary[/bold]", SUMMARY)
    console.print(branded_panel(TAGLINE, title=APP_NAME))
    console.print(table)
