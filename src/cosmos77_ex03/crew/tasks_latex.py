"""LaTeX-author task (Phase 8): the LLM Markdown->LaTeX conversion option (B13).

Encodes the latex-author Skill's contract as a CrewAI Task. The default build
path (``SDK.assemble_latex`` -> ``latex.assemble``) is deterministic for a
guaranteed clean compile; this task is the LLM alternative for the latex_author
agent and is unit-tested for correct wiring.
"""

from __future__ import annotations

from typing import Any

from crewai import Task


def latex_author_task(
    latex_author: Any, chapter_md: str, output_file: str, *, hebrew: bool = False
) -> Task:
    """Build a task converting one chapter's Markdown to a clean LaTeX fragment."""
    bidi = (
        " This is the Hebrew chapter: use \\selectlanguage{hebrew} for the body, wrap inline "
        "English in \\foreignlanguage{english}{...}, and keep it right-to-left."
        if hebrew
        else ""
    )
    description = (
        "Convert the chapter Markdown below into a clean LuaLaTeX fragment using \\section, "
        "fancy amsmath where useful, tabularx (never \\hline), and \\cite keys matching "
        f"refs.bib.{bidi} Emit ONLY LaTeX — no code fences, no 'Here is' preamble.\n\n" + chapter_md
    )
    return Task(
        description=description,
        expected_output="A valid LuaLaTeX fragment (no preamble, no document environment).",
        agent=latex_author,
        output_file=output_file,
        markdown=False,
    )
