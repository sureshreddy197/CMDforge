"""Environment diagnostics for the ``doctor`` command."""

from __future__ import annotations

import platform
import sys
from dataclasses import dataclass
from pathlib import Path

from .config import config_file_exists
from .metadata import VERSION
from .paths import get_cache_dir, get_config_dir, get_config_file


@dataclass(frozen=True)
class DiagnosticReport:
    """Collected environment information for display."""

    python_version: str
    python_implementation: str
    platform_name: str
    executable_path: Path
    package_version: str
    config_directory: Path
    cache_directory: Path
    config_file: Path
    config_file_exists: bool
    current_working_directory: Path


def collect_diagnostics() -> DiagnosticReport:
    """Gather deterministic environment details used by the CLI."""

    return DiagnosticReport(
        python_version=platform.python_version(),
        python_implementation=platform.python_implementation(),
        platform_name=platform.platform(),
        executable_path=Path(sys.executable).resolve(),
        package_version=VERSION,
        config_directory=get_config_dir(),
        cache_directory=get_cache_dir(),
        config_file=get_config_file(),
        config_file_exists=config_file_exists(),
        current_working_directory=Path.cwd(),
    )
