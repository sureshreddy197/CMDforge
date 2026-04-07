"""Persistent configuration management."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from pathlib import Path
from typing import Any, TypeAlias

try:
    import tomllib  # type: ignore[import-not-found]
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib

from .exceptions import ConfigError, ConfigKeyError
from .paths import ensure_config_dir, get_config_file

ConfigValue: TypeAlias = str | bool
Parser: TypeAlias = Callable[[str], ConfigValue]

SUPPORTED_LICENSES = frozenset({"MIT", "Apache-2.0", "BSD-3-Clause"})
SUPPORTED_COLOR_SYSTEMS = frozenset({"auto", "standard", "256", "truecolor", "windows", "none"})


@dataclass(frozen=True)
class ConfigField:
    """Typed metadata describing a configuration key."""

    default: ConfigValue
    description: str
    parser: Parser
    allowed_values: frozenset[str] | None = None


def _parse_bool(value: str) -> bool:
    normalized = value.strip().lower()
    truthy = {"1", "true", "yes", "on"}
    falsy = {"0", "false", "no", "off"}
    if normalized in truthy:
        return True
    if normalized in falsy:
        return False
    raise ConfigError(
        "Invalid boolean value. Use one of: true, false, yes, no, on, off, 1, 0."
    )


FIELD_SPECS: dict[str, ConfigField] = {
    "color_system": ConfigField(
        default="auto",
        description="Preferred Rich color mode.",
        parser=str,
        allowed_values=SUPPORTED_COLOR_SYSTEMS,
    ),
    "confirm_destructive_actions": ConfigField(
        default=True,
        description="Prompt before reset and cache clear actions.",
        parser=_parse_bool,
    ),
    "scaffold_license": ConfigField(
        default="MIT",
        description="Default license used by `cmdforge init`.",
        parser=str,
        allowed_values=SUPPORTED_LICENSES,
    ),
    "scaffold_include_github_actions": ConfigField(
        default=True,
        description="Include a GitHub Actions workflow in generated scaffolds.",
        parser=_parse_bool,
    ),
    "scaffold_include_pre_commit": ConfigField(
        default=True,
        description="Include pre-commit configuration in generated scaffolds.",
        parser=_parse_bool,
    ),
}

DEFAULT_CONFIG: dict[str, ConfigValue] = {
    key: field.default for key, field in FIELD_SPECS.items()
}


@dataclass(frozen=True)
class ConfigEntry:
    """A rendered configuration value with metadata for tables."""

    key: str
    value: ConfigValue
    source: str
    description: str


def get_config_path() -> Path:
    """Return the path to the user configuration file."""

    return get_config_file()


def config_file_exists() -> bool:
    """Return whether the config file is present on disk."""

    return get_config_path().is_file()


def get_supported_keys() -> list[str]:
    """Return all valid configuration keys in sorted order."""

    return sorted(FIELD_SPECS)


def validate_key(key: str) -> ConfigField:
    """Return field metadata for *key* or raise a friendly error."""

    try:
        return FIELD_SPECS[key]
    except KeyError as exc:
        valid = ", ".join(get_supported_keys())
        raise ConfigKeyError(f"Unknown config key '{key}'. Valid keys: {valid}.") from exc


def _format_toml_value(value: ConfigValue) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def _parse_user_value(key: str, value: Any) -> ConfigValue:
    field = validate_key(key)
    if isinstance(field.default, bool):
        if not isinstance(value, bool):
            raise ConfigError(f"Expected a boolean value for '{key}' in {get_config_path()}.")
    elif not isinstance(value, str):
        raise ConfigError(f"Expected a string value for '{key}' in {get_config_path()}.")

    parsed = value if isinstance(value, bool) else field.parser(str(value))
    _validate_allowed_value(key, parsed)
    return parsed


def _validate_allowed_value(key: str, value: ConfigValue) -> None:
    field = validate_key(key)
    if field.allowed_values is None:
        return
    if not isinstance(value, str) or value not in field.allowed_values:
        allowed = ", ".join(sorted(field.allowed_values))
        raise ConfigError(f"Invalid value for '{key}'. Allowed values: {allowed}.")


def read_user_config() -> dict[str, ConfigValue]:
    """Read user-defined values from disk.

    Missing files return an empty mapping. Unknown keys are ignored so the
    application remains forward-compatible across releases.
    """

    path = get_config_path()
    if not path.exists():
        return {}

    try:
        parsed = tomllib.loads(path.read_text(encoding="utf-8"))
    except tomllib.TOMLDecodeError as exc:
        raise ConfigError(f"Could not parse configuration file at {path}: {exc}.") from exc
    except OSError as exc:
        raise ConfigError(f"Could not read configuration file at {path}: {exc}.") from exc

    section = parsed.get("cmdforge", {})
    if not isinstance(section, dict):
        raise ConfigError(f"The [cmdforge] section in {path} must be a table.")

    normalized: dict[str, ConfigValue] = {}
    for key, value in section.items():
        if key not in FIELD_SPECS:
            continue
        normalized[key] = _parse_user_value(key, value)
    return normalized


def get_effective_config() -> dict[str, ConfigValue]:
    """Return defaults merged with any stored user overrides."""

    effective = DEFAULT_CONFIG.copy()
    effective.update(read_user_config())
    return effective


def describe_config() -> list[ConfigEntry]:
    """Return configuration metadata for table rendering."""

    user_values = read_user_config()
    effective = get_effective_config()
    entries: list[ConfigEntry] = []
    for key in get_supported_keys():
        source = "user" if key in user_values else "default"
        entries.append(
            ConfigEntry(
                key=key,
                value=effective[key],
                source=source,
                description=FIELD_SPECS[key].description,
            )
        )
    return entries


def get_config_value(key: str) -> ConfigValue:
    """Return the effective value for *key*."""

    validate_key(key)
    return get_effective_config()[key]


def set_config_value(key: str, raw_value: str) -> ConfigValue:
    """Parse, validate, and persist a single configuration value."""

    field = validate_key(key)
    if isinstance(field.default, bool):
        value = field.parser(raw_value)
    else:
        value = field.parser(raw_value.strip())
    _validate_allowed_value(key, value)

    user_values = read_user_config()
    user_values[key] = value
    _write_user_config(user_values)
    return value


def reset_config() -> bool:
    """Reset the user configuration by removing the config file.

    Returns ``True`` when a file was removed and ``False`` when there was
    nothing to delete.
    """

    path = get_config_path()
    if not path.exists():
        return False
    try:
        path.unlink()
    except OSError as exc:
        raise ConfigError(f"Could not remove configuration file at {path}: {exc}.") from exc
    return True


def _write_user_config(values: dict[str, ConfigValue]) -> None:
    ensure_config_dir()
    path = get_config_path()
    lines = ["[cmdforge]"]
    for key in get_supported_keys():
        if key not in values:
            continue
        lines.append(f"{key} = {_format_toml_value(values[key])}")
    content = "\n".join(lines) + "\n"
    try:
        path.write_text(content, encoding="utf-8")
    except OSError as exc:
        raise ConfigError(f"Could not write configuration file at {path}: {exc}.") from exc
