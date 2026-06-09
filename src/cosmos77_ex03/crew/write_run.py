"""Run the parallel chapter-writing crew and stitch the article (Phase 6).

Builds one writer per chapter (the Hebrew BiDi chapter → ``bidi_writer``), runs
them ``async_execution=True`` when ``crew.parallel_writers`` is set, throttled by
``crew.max_rpm`` for the free tier, then an editor stitches ``output/article.md``.
A deterministic fallback guarantees ``article.md`` is complete.
"""

from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING, Any

from crewai import Crew, Process

from cosmos77_ex03.crew.agents import bidi_writer as build_bidi_writer
from cosmos77_ex03.crew.agents import chapter_writer as build_chapter_writer
from cosmos77_ex03.crew.agents import editor as build_editor
from cosmos77_ex03.crew.schemas import Outline
from cosmos77_ex03.crew.tasks_write import editor_task, write_task
from cosmos77_ex03.providers.factory import build_llm

if TYPE_CHECKING:
    from cosmos77_ex03.shared.config import Config


def run_write(cfg: Config) -> tuple[int, Any]:
    """Write every chapter (BiDi → bidi_writer), edit, and stitch article.md."""
    out_dir = cfg.paths().get("output_dir", "output")
    outline = Outline.model_validate_json(Path(out_dir, "outline.json").read_text(encoding="utf-8"))
    Path(out_dir, "chapters").mkdir(parents=True, exist_ok=True)
    llm = build_llm(cfg)
    parallel = bool(cfg.get("crew.parallel_writers", True))
    editor = build_editor(llm)
    agents: list[Any] = [editor]
    writes: list[Any] = []
    for chapter in outline.chapters:
        writer = (
            build_bidi_writer(llm) if chapter.is_bidi else build_chapter_writer(llm, chapter.index)
        )
        agents.append(writer)
        writes.append(write_task(writer, chapter, out_dir, async_exec=parallel))
    tasks = [*writes, editor_task(editor, writes, out_dir)]
    crew = Crew(
        agents=agents,
        tasks=tasks,
        process=Process.sequential,
        max_rpm=int(cfg.get("crew.max_rpm", 10)),
        verbose=False,
    )
    result = crew.kickoff()
    _ensure_article(out_dir, outline)
    return len(outline.chapters), getattr(result, "token_usage", None)


def _ensure_article(out_dir: str, outline: Outline) -> None:
    """Guarantee article.md exists by stitching the chapters if the editor's is thin."""
    article = Path(out_dir, "article.md")
    if article.exists() and len(article.read_text(encoding="utf-8").strip()) > 200:
        return
    parts: list[str] = []
    for chapter in outline.chapters:
        path = Path(out_dir, "chapters", f"ch_{chapter.index:02d}.md")
        if path.exists():
            parts.append(path.read_text(encoding="utf-8").strip())
    article.write_text("\n\n".join(parts) + "\n", encoding="utf-8")
