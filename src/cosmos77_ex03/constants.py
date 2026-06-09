"""Project-wide structural constants (not tunable config — see CLAUDE.md rule 4).

These are fixed enumerations the crew, tasks, and SDK share. Tunable values
(topic, language, model, provider, chapter count, paths) live in ``config/*.json``
and are read via the Config loader.
"""

from __future__ import annotations

#: Default text encoding for all file I/O across the project.
DEFAULT_ENCODING: str = "utf-8"

#: The importable package name (mirrors pyproject ``name``, underscored).
PACKAGE_NAME: str = "cosmos77_ex03"

#: The version string — kept in lockstep with pyproject and every config file.
PROJECT_VERSION: str = "1.00"

#: The fixed CrewAI agent roles (one ``Agent`` builder per role; writers fan out).
AGENT_ROLES: tuple[str, ...] = (
    "researcher",
    "planner",
    "chapter_writer",
    "figure_agent",
    "bidi_writer",
    "editor",
    "latex_author",
)

#: The lifecycle a chapter passes through, in order.
CHAPTER_STATUSES: tuple[str, ...] = ("pending", "drafting", "written", "edited", "typeset")
