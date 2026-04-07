"""Application-specific exceptions and exit codes."""

from __future__ import annotations

from enum import IntEnum


class ExitCode(IntEnum):
    """Stable process exit codes used by the CLI."""

    SUCCESS = 0
    ERROR = 1
    INVALID_INPUT = 2
    NOT_FOUND = 3


class CmdforgeError(RuntimeError):
    """Base class for domain errors with friendly CLI messages."""


class ConfigError(CmdforgeError):
    """Raised when the configuration file is invalid or cannot be read."""


class ConfigKeyError(ConfigError):
    """Raised when an unknown configuration key is requested."""


class ScaffoldError(CmdforgeError):
    """Raised when scaffold generation cannot proceed safely."""
