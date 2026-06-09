"""CrewAI agent factories — the article-writing team (B10, B13).

Each builder returns a configured ``Agent`` (role/goal/backstory/llm/tools/skills),
``allow_delegation=False`` (workers never delegate — ADR-002), ``verbose=False``.
Skills are wired by absolute path to ``src/cosmos77_ex03/skills/<name>`` so they
resolve regardless of the working directory. Chapter writers are a factory (one
Agent per chapter) for the async parallel write phase.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

from crewai import Agent

from cosmos77_ex03.crew.tools import file_writer_tools, web_search_tools

if TYPE_CHECKING:
    from cosmos77_ex03.shared.config import Config

_SKILLS_DIR = Path(__file__).resolve().parent.parent / "skills"


def skill_path(name: str) -> str:
    """Return the absolute path to the SKILL.md package dir for ``name``."""
    return str(_SKILLS_DIR / name)


def make_agent(
    *,
    role: str,
    goal: str,
    backstory: str,
    llm: Any,
    tools: list[Any] | None = None,
    skills: list[str] | None = None,
) -> Agent:
    """Construct an Agent with project defaults (no delegation, non-verbose)."""
    return Agent(
        role=role,
        goal=goal,
        backstory=backstory,
        llm=llm,
        tools=tools or [],
        skills=skills or [],
        allow_delegation=False,
        verbose=False,
    )


def researcher(llm: Any) -> Agent:
    """Gather citation-backed facts grounded in the 2026 source + web."""
    return make_agent(
        role="Senior AI Research Analyst",
        goal="Gather accurate, citation-backed facts on production AI agents.",
        backstory="You ground every claim in the 2026 architecture source or reputable sources; you never invent citations.",
        llm=llm,
        tools=web_search_tools(),
        skills=[skill_path("researcher")],
    )


def planner(llm: Any) -> Agent:
    """Turn research into a coherent 12-chapter outline."""
    return make_agent(
        role="Technical Content Architect",
        goal="Produce a logical 12-chapter outline for a ~15-page article.",
        backstory="You structure complex topics into chapters, reserving one for a Hebrew BiDi treatment.",
        llm=llm,
        skills=[skill_path("technical-writer")],
    )


def chapter_writer(llm: Any, index: int | None = None) -> Agent:
    """Factory: one chapter-writer Agent (instantiated per chapter for parallelism)."""
    suffix = f" #{index}" if index is not None else ""
    return make_agent(
        role=f"Technical Chapter Writer{suffix}",
        goal="Write one clear, cited ~1-page chapter in the house style.",
        backstory="You turn research into accurate engineering prose; every claim carries a cite marker.",
        llm=llm,
        skills=[skill_path("technical-writer")],
    )


def figure_agent(llm: Any) -> Agent:
    """Specify the data and captions for the article's figures."""
    return make_agent(
        role="Data Visualization Specialist",
        goal="Specify accurate, well-captioned data figures for the article.",
        backstory="You translate quantitative claims into clear, honest charts.",
        llm=llm,
        skills=[skill_path("technical-writer")],
    )


def bidi_writer(llm: Any) -> Agent:
    """Write the Hebrew-English BiDi chapter."""
    return make_agent(
        role="Hebrew Technical Writer",
        goal="Write one Hebrew chapter with correctly directioned inline English terms.",
        backstory="You write right-to-left Hebrew prose, keeping English technical terms inline and correct.",
        llm=llm,
        skills=[skill_path("technical-writer")],
    )


def editor(llm: Any) -> Agent:
    """Review cross-chapter consistency and citation completeness."""
    return make_agent(
        role="Managing Editor",
        goal="Ensure one voice, dedupe content, and a citation in every chapter.",
        backstory="You enforce consistent terminology and verify every chapter cites at least one source.",
        llm=llm,
        skills=[skill_path("technical-writer")],
    )


def latex_author(llm: Any) -> Agent:
    """Convert finished Markdown into clean, compiling LuaLaTeX."""
    return make_agent(
        role="LaTeX Typesetter",
        goal="Emit only valid LuaLaTeX: fancy math, non-overflow tables, linked cites, correct BiDi.",
        backstory="You produce .tex that survives lualatex/biber/lualatex/lualatex with zero undefined references.",
        llm=llm,
        tools=file_writer_tools(),
        skills=[skill_path("latex-author")],
    )


def build_agents(cfg: Config) -> dict[str, Agent]:
    """Build the crew's singleton agents (chapter writers are made per-chapter)."""
    from cosmos77_ex03.providers.factory import build_llm

    llm = build_llm(cfg)
    return {
        "researcher": researcher(llm),
        "planner": planner(llm),
        "figure_agent": figure_agent(llm),
        "bidi_writer": bidi_writer(llm),
        "editor": editor(llm),
        "latex_author": latex_author(llm),
    }
