"""Filesystem path helpers for CMDforge."""

from __future__ import annotations

from pathlib import Path

from platformdirs import PlatformDirs

from .metadata import PACKAGE_NAME


def _platform_dirs() -> PlatformDirs:
    return PlatformDirs(appname=PACKAGE_NAME, appauthor=False, roaming=True)


def get_config_dir() -> Path:
    return Path(_platform_dirs().user_config_dir)


def get_cache_dir() -> Path:
    return Path(_platform_dirs().user_cache_dir)


def get_config_file() -> Path:
    return get_config_dir() / "config.toml"


def ensure_config_dir() -> Path:
    path = get_config_dir()
    path.mkdir(parents=True, exist_ok=True)
    return path


def ensure_cache_dir() -> Path:
    path = get_cache_dir()
    path.mkdir(parents=True, exist_ok=True)
    return path
