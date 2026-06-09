"""Research + outline tasks (Phase 5): a cited 12-chapter plan.

``research_task`` grounds on an excerpt of the local 2026 source PDF (injected as
context — more robust than a RAG tool) plus the agent's knowledge, and writes
``output/research.md``. ``outline_task`` returns a validated :class:`Outline`
(structured JSON) so the chapter list and citations are machine-readable.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from crewai import Task

from cosmos77_ex03.crew.schemas import Outline

if TYPE_CHECKING:
    from crewai import Agent

TOPIC = "AI Agents in Production: Architecture, Orchestration & Governance in 2026"


def reference_excerpt(pdf_path: str | Path, max_chars: int = 12000) -> str:
    """Extract grounding text from the reference PDF; '' if missing/unreadable."""
    path = Path(pdf_path)
    if not path.exists():
        return ""
    try:
        import pdfplumber

        with pdfplumber.open(str(path)) as pdf:
            text = "\n".join((page.extract_text() or "") for page in pdf.pages)
        return text[:max_chars]
    except Exception:
        return ""


def research_task(researcher: Agent, output_dir: str, reference_pdf: str | Path = "") -> Task:
    """Task: gather cited facts grounded in the 2026 source + the agent's knowledge."""
    grounding = reference_excerpt(reference_pdf) if reference_pdf else ""
    block = f"\n\n=== PRIMARY SOURCE EXCERPT ===\n{grounding}\n=== END ===" if grounding else ""
    description = (
        f"Research the topic '{TOPIC}'. Produce a structured Markdown fact list where "
        f"every nontrivial claim names a source; prefer the primary source and reputable "
        f"references (framework docs, OWASP, Gartner). End with a '## Sources' section of "
        f"BibTeX-ready entries (key, author, title, year, venue, url). Do not invent sources."
        f"{block}"
    )
    return Task(
        description=description,
        expected_output="A Markdown fact+source list ending with a '## Sources' section.",
        agent=researcher,
        output_file=f"{output_dir}/research.md",
        markdown=True,
    )


def outline_task(planner: Agent, context: list[Task], num_chapters: int) -> Task:
    """Task: produce a structured :class:`Outline` (chapters + citations) as JSON."""
    description = (
        f"Using the research, design exactly {num_chapters} chapters for a ~15-page article "
        f"on '{TOPIC}'. Cover: the 2025->2026 inflection, agent anatomy, orchestration, "
        f"framework selection, RAG/type-safety/prompt-optimization, MCP/A2A protocols, "
        f"multi-agent governance, security (OWASP), observability, the PoC->production gap, "
        f"TCO, and a roadmap. Mark EXACTLY ONE chapter is_bidi=true (the Hebrew BiDi chapter). "
        f"For each chapter give index (1-based), title, a one-line brief, and citation_keys "
        f"drawn from the research. Also return the full citations list."
    )
    return Task(
        description=description,
        expected_output=f"A JSON object: {num_chapters} chapters plus a citations list.",
        agent=planner,
        context=context,
        output_pydantic=Outline,
    )
