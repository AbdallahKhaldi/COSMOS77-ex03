"""Project-wide constants.

Expanded with crew role / chapter-status constants in Phase 2; kept tiny and
side-effect-free so importing it is the only thing tests need to exercise it.
"""

from __future__ import annotations

#: Default text encoding for all file I/O across the project.
DEFAULT_ENCODING: str = "utf-8"

#: The importable package name (mirrors pyproject ``name``, underscored).
PACKAGE_NAME: str = "cosmos77_ex03"

#: The version string — kept in lockstep with pyproject and every config file.
PROJECT_VERSION: str = "1.00"
