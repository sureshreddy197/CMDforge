"""Console rendering helpers built on Rich."""

from __future__ import annotations

from functools import lru_cache
from typing import Final, Literal, cast

from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from .metadata import APP_NAME

DEFAULT_WIDTH: Final[int] = 100
ColorSystem = Literal["auto", "standard", "256", "truecolor", "windows"]


@lru_cache(maxsize=1)
def get_console() -> Console:
    """Return a shared console instance.

    The color system can be influenced by user configuration. Configuration
    errors intentionally fall back to automatic color detection so command
    output remains available even if the config file is broken.
    """

    color_system: ColorSystem | None = "auto"
    try:
        from .config import get_config_value

        configured = str(get_config_value("color_system"))
        color_system = None if configured == "none" else cast(ColorSystem, configured)
    except Exception:
        color_system = "auto"

    return Console(highlight=False, color_system=color_system, soft_wrap=True, width=DEFAULT_WIDTH)


def print_error(message: str) -> None:
    """Print an error message in a consistent style."""

    get_console().print(f"[bold red]Error:[/bold red] {message}")


def print_success(message: str) -> None:
    """Print a success message in a consistent style."""

    get_console().print(f"[bold green]OK:[/bold green] {message}")


def print_warning(message: str) -> None:
    """Print a warning message in a consistent style."""

    get_console().print(f"[bold yellow]Note:[/bold yellow] {message}")


def branded_panel(body: str, *, title: str | None = None) -> Panel:
    """Return a reusable panel with CMDforge branding."""

    panel_title = title or APP_NAME
    return Panel.fit(Text.from_markup(body), title=panel_title, border_style="cyan")
