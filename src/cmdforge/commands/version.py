"""Implementation for the ``version`` command."""

from __future__ import annotations

from ..metadata import VERSION


def run() -> str:
    """Return the package version for clean CLI output."""

    return VERSION
