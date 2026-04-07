"""Typer application entrypoint for CMDforge."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Annotated

import typer

from .commands import about as about_command
from .commands import cache as cache_command
from .commands import config as config_command
from .commands import doctor as doctor_command
from .commands import init as init_command
from .commands import version as version_command
from .config import get_config_value
from .console import print_error
from .exceptions import CmdforgeError, ConfigError, ConfigKeyError, ExitCode, ScaffoldError
from .metadata import CLI_NAME, SUMMARY

CONTEXT_SETTINGS = {"help_option_names": ["-h", "--help"]}

app = typer.Typer(
    add_completion=False,
    no_args_is_help=True,
    rich_markup_mode="rich",
    help=SUMMARY,
    epilog="Examples:\n  cmdforge doctor\n  cmdforge config show\n  cmdforge init hello-cli",
    context_settings=CONTEXT_SETTINGS,
)
config_app = typer.Typer(help="Inspect and manage persistent CMDforge settings.")
cache_app = typer.Typer(help="Inspect and manage CMDforge cache files.")
app.add_typer(config_app, name="config")
app.add_typer(cache_app, name="cache")


@app.command("about")
def about() -> None:
    """Show project overview, version, and repository details."""

    about_command.run()


@app.command("version")
def version() -> None:
    """Print the installed package version."""

    typer.echo(version_command.run())


@app.command("doctor")
def doctor() -> None:
    """Show environment diagnostics for the current installation."""

    doctor_command.run()


@config_app.command("show")
def config_show() -> None:
    """Show the effective configuration values."""

    _run_guarded(config_command.show)


@config_app.command("get")
def config_get(
    key: Annotated[str, typer.Argument(help="Config key to read.")],
) -> None:
    """Read a single configuration value."""

    try:
        typer.echo(config_command.get_value(key))
    except ConfigKeyError as exc:
        print_error(str(exc))
        raise typer.Exit(code=ExitCode.INVALID_INPUT.value) from exc
    except ConfigError as exc:
        print_error(str(exc))
        raise typer.Exit(code=ExitCode.ERROR.value) from exc


@config_app.command("set")
def config_set(
    key: Annotated[str, typer.Argument(help="Config key to update.")],
    value: Annotated[str, typer.Argument(help="Value to persist.")],
) -> None:
    """Persist a configuration value."""

    try:
        config_command.set_value(key, value)
    except (ConfigKeyError, ConfigError) as exc:
        print_error(str(exc))
        raise typer.Exit(code=ExitCode.INVALID_INPUT.value) from exc


@config_app.command("reset")
def config_reset(
    yes: Annotated[
        bool,
        typer.Option("--yes", help="Skip the confirmation prompt."),
    ] = False,
) -> None:
    """Reset the user config file and restore defaults."""

    try:
        should_confirm = bool(get_config_value("confirm_destructive_actions")) and not yes
    except ConfigError:
        should_confirm = not yes

    if should_confirm:
        confirmed = typer.confirm("Reset CMDforge configuration to defaults?", default=False)
        if not confirmed:
            raise typer.Exit(code=ExitCode.SUCCESS.value)

    _run_guarded(config_command.reset)


@cache_app.command("info")
def cache_info() -> None:
    """Show cache location and basic statistics."""

    cache_command.info()


@cache_app.command("clear")
def cache_clear(
    yes: Annotated[
        bool,
        typer.Option("--yes", help="Skip the confirmation prompt."),
    ] = False,
) -> None:
    """Remove files created in the application cache directory."""

    try:
        should_confirm = bool(get_config_value("confirm_destructive_actions")) and not yes
    except ConfigError:
        should_confirm = not yes

    if should_confirm:
        confirmed = typer.confirm("Clear CMDforge cache files?", default=False)
        if not confirmed:
            raise typer.Exit(code=ExitCode.SUCCESS.value)

    cache_command.clear()


@app.command("init")
def init(
    project_name: Annotated[str, typer.Argument(help="Name of the project to generate.")],
    directory: Annotated[
        Path | None,
        typer.Option(
            "--directory",
            "-d",
            help="Target directory. Defaults to ./<project_name>.",
            file_okay=False,
            dir_okay=True,
            resolve_path=True,
        ),
    ] = None,
    force: Annotated[
        bool,
        typer.Option("--force", help="Overwrite files in an existing target directory."),
    ] = False,
) -> None:
    """Generate a clean starter CLI scaffold."""

    try:
        init_command.run(project_name, directory=directory, force=force)
    except ScaffoldError as exc:
        print_error(str(exc))
        raise typer.Exit(code=ExitCode.INVALID_INPUT.value) from exc
    except ConfigError as exc:
        print_error(str(exc))
        raise typer.Exit(code=ExitCode.ERROR.value) from exc


def _run_guarded(callback: Callable[[], None]) -> None:
    try:
        callback()
    except ConfigKeyError as exc:
        print_error(str(exc))
        raise typer.Exit(code=ExitCode.INVALID_INPUT.value) from exc
    except ConfigError as exc:
        print_error(str(exc))
        raise typer.Exit(code=ExitCode.ERROR.value) from exc
    except CmdforgeError as exc:
        print_error(str(exc))
        raise typer.Exit(code=ExitCode.ERROR.value) from exc


def main() -> None:
    """Console script entrypoint."""

    try:
        app(prog_name=CLI_NAME)
    except KeyboardInterrupt as exc:
        print_error("Interrupted.")
        raise SystemExit(130) from exc


if __name__ == "__main__":  # pragma: no cover
    main()
