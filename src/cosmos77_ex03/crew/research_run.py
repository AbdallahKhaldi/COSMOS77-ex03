"""Run the research + outline crew and persist artifacts (Phase 5).

Sequential two-task crew: the researcher writes ``output/research.md``; the
planner returns a validated :class:`Outline`, which we persist as
``output/outline.json`` (full), ``output/citations.json`` (the citation pool),
and a human-readable ``output/outline.md``.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import TYPE_CHECKING, Any

from crewai import Crew, Process

from cosmos77_ex03.crew.agents import planner as build_planner
from cosmos77_ex03.crew.agents import researcher as build_researcher
from cosmos77_ex03.crew.schemas import Outline
from cosmos77_ex03.crew.tasks_research import outline_task, research_task
from cosmos77_ex03.providers.factory import build_llm

if TYPE_CHECKING:
    from cosmos77_ex03.shared.config import Config


def _reference_path(cfg: Config) -> str:
    """Resolve the reference PDF path (relative to the repo root) from config."""
    rel = cfg.paths().get("reference_pdf", "")
    if not rel:
        return ""
    return str((Path(cfg.config_dir).parent / rel).resolve())


def run_research(cfg: Config) -> tuple[Outline, Any]:
    """Run research + outline; persist artifacts; return ``(outline, token_usage)``."""
    out_dir = cfg.paths().get("output_dir", "output")
    Path(out_dir, "chapters").mkdir(parents=True, exist_ok=True)
    llm = build_llm(cfg)
    researcher = build_researcher(llm)
    planner = build_planner(llm)
    rtask = research_task(researcher, out_dir, _reference_path(cfg))
    otask = outline_task(planner, [rtask], int(cfg.get("crew.num_chapters", 12)))
    crew = Crew(
        agents=[researcher, planner],
        tasks=[rtask, otask],
        process=Process.sequential,
        max_rpm=int(cfg.get("crew.max_rpm", 10)),
        verbose=False,
    )
    result = crew.kickoff()
    outline = getattr(result, "pydantic", None) or Outline.model_validate_json(result.raw)
    _persist(out_dir, outline)
    return outline, getattr(result, "token_usage", None)


def _persist(out_dir: str, outline: Outline) -> None:
    """Write outline.json, citations.json, and a human-readable outline.md."""
    base = Path(out_dir)
    base.joinpath("outline.json").write_text(outline.model_dump_json(indent=2), encoding="utf-8")
    citations = [c.model_dump() for c in outline.citations]
    base.joinpath("citations.json").write_text(
        json.dumps(citations, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    lines = ["# Outline\n"]
    for ch in outline.chapters:
        tag = " (Hebrew BiDi)" if ch.is_bidi else ""
        lines.append(f"{ch.index}. **{ch.title}**{tag} — {ch.brief}")
    base.joinpath("outline.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
