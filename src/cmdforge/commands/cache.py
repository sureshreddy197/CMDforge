"""Implementation for the ``cache`` command group."""

from __future__ import annotations

import shutil
from pathlib import Path

from rich.filesize import decimal
from rich.panel import Panel
from rich.table import Table

from ..console import get_console, print_success, print_warning
from ..paths import get_cache_dir


def _cache_stats(root: Path) -> tuple[int, int]:
    file_count = 0
    total_bytes = 0
    if not root.exists():
        return file_count, total_bytes
    for path in root.rglob("*"):
        if path.is_file():
            file_count += 1
            total_bytes += path.stat().st_size
    return file_count, total_bytes


def info() -> None:
    """Show cache location and simple filesystem statistics."""

    cache_dir = get_cache_dir()
    file_count, total_bytes = _cache_stats(cache_dir)

    table = Table(show_header=False, box=None, expand=False, padding=(0, 1))
    table.add_row("Location", str(cache_dir))
    table.add_row("Exists", "yes" if cache_dir.exists() else "no")
    table.add_row("Files", str(file_count))
    table.add_row("Size", decimal(total_bytes))

    get_console().print(Panel.fit(table, title="CMDforge cache", border_style="cyan"))


def clear() -> None:
    """Remove all files in the application cache directory."""

    cache_dir = get_cache_dir()
    if not cache_dir.exists():
        print_warning("Cache directory does not exist yet. Nothing to clear.")
        return

    for entry in cache_dir.iterdir():
        if entry.is_dir():
            shutil.rmtree(entry)
        else:
            entry.unlink()
    print_success(f"Cleared cache at {cache_dir}.")
