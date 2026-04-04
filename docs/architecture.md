# Architecture

CMDforge is intentionally small, but it is structured like a production repository rather than a one-file demo.
The goal is to make the code easy to read, extend, and trust.

## Module layout

### `src/cmdforge/metadata.py`

Central project metadata such as branding, version, summary, and repository URL.
Keeping this in one place avoids string drift between commands, docs, and tests.

### `src/cmdforge/cli.py`

The Typer application entrypoint.
It wires command groups, defines the public CLI surface, and maps domain errors to stable exit codes.

### `src/cmdforge/commands/`

Thin command modules for user-facing behavior:

- `about.py`
- `version.py`
- `doctor.py`
- `config.py`
- `cache.py`
- `init.py`

These modules focus on orchestration and presentation instead of owning persistence or path logic.

### `src/cmdforge/config.py`

The TOML-backed configuration layer.
Responsibilities:

- define supported keys and defaults
- validate config values
- parse and write the user config file
- expose effective config values for commands

The config file is intentionally flat inside a `[cmdforge]` table so it stays easy to inspect and edit.

### `src/cmdforge/paths.py`

A small path abstraction over `platformdirs`.
This keeps platform-specific directory resolution in one place and makes the rest of the code easier to test.

### `src/cmdforge/doctor.py`

Pure diagnostics collection.
This module gathers environment facts and returns a typed report object that the command layer renders.

### `src/cmdforge/scaffold.py`

Project scaffold generation.
This module owns:

- project-name normalization
- package and command-name derivation
- target safety checks
- rendering concrete file contents
- writing the generated project to disk

The scaffold logic is deliberately template-driven and explicit.
That keeps it maintainable and avoids hidden magic.

### `src/cmdforge/console.py`

Shared Rich console helpers and output styling.
This is intentionally lightweight: it centralizes branding and message styles without becoming a custom UI framework.

## Command design

The CLI uses a straightforward split:

- root commands for high-level tasks (`about`, `version`, `doctor`, `init`)
- grouped subcommands for related stateful operations (`config`, `cache`)

This keeps the mental model clear while leaving room for future expansion.

## Config handling

CMDforge stores config in the correct platform-specific user config directory.
The file format is TOML because it is readable, editable, and a good fit for small local settings.

Design choices:

- defaults always work without a file on disk
- unknown keys from older or newer versions are ignored when reading
- invalid values produce clean errors
- destructive commands can use config-driven confirmation behavior

## Scaffold generation approach

The scaffold generator is intentionally practical rather than generic.
It writes a real starter repository with packaging, tests, and optional CI / pre-commit support.

Notable choices:

- `src/` layout for modern packaging hygiene
- a very small Typer app with real tests
- a real `LICENSE` file using supported SPDX choices
- optional CI and pre-commit toggled from CMDforge config

## Testing philosophy

Tests focus on the actual CLI behaviors users care about:

- help output
- version and about output
- diagnostics rendering
- config write/read/reset flows
- scaffold filesystem output

The project avoids tests that only assert private implementation details.
