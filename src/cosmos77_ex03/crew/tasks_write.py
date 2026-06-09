"""Chapter-writing + editor tasks (Phase 6): the article body (B1, B8, B10).

One async ``write_task`` per chapter (the Hebrew BiDi chapter routes to the
``bidi_writer``); a final sync ``editor_task`` reviews consistency and emits a
stitched ``output/article.md``. Phase 8 typesets from the per-chapter files.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from crewai import Task

if TYPE_CHECKING:
    from cosmos77_ex03.crew.schemas import Chapter


def write_task(writer: Any, chapter: Chapter, output_dir: str, *, async_exec: bool = True) -> Task:
    """Build the write task for one chapter (Hebrew body if ``chapter.is_bidi``)."""
    keys = ", ".join(chapter.citation_keys) or "the research sources"
    if chapter.is_bidi:
        lang = (
            "CRITICAL LANGUAGE REQUIREMENT: write the ENTIRE chapter body in the HEBREW "
            "language (עברית), right-to-left — full Hebrew sentences, NOT English. Only inline "
            "technical terms stay in English (e.g. 'RAG', 'MCP', 'the Harness', 'observability'); "
            "the heading and all prose must be Hebrew. "
        )
    else:
        lang = "Write in clear, active English. "
    description = (
        f"Write chapter {chapter.index}: '{chapter.title}'. Brief: {chapter.brief}. "
        f"{lang}Target ~1 to 1.25 pages (~550-650 words). Cite sources inline with "
        f"\\cite{{key}} using these keys: {keys}. Begin with a single '## ' heading; every "
        f"nontrivial claim cites a source; end with a one-sentence bridge. Output ONLY the "
        f"Markdown content: NO triple-backtick code fences and NO 'Here is...' preamble."
    )
    return Task(
        description=description,
        expected_output="~1 page of Markdown: a single ## heading and inline \\cite{...} markers.",
        agent=writer,
        output_file=f"{output_dir}/chapters/ch_{chapter.index:02d}.md",
        markdown=True,
        async_execution=async_exec,
    )


def editor_task(editor: Any, write_tasks: list[Task], output_dir: str) -> Task:
    """Build the editor task that reviews consistency and stitches ``article.md``."""
    description = (
        "Assemble the chapters into one cohesive Markdown article. Fix only consistency, "
        "terminology, and transitions; PRESERVE every chapter's content, all \\cite{...} "
        "markers, and the Hebrew chapter verbatim. Ensure each chapter cites >=1 source."
    )
    return Task(
        description=description,
        expected_output="The full article as Markdown, chapters in order.",
        agent=editor,
        context=write_tasks,
        output_file=f"{output_dir}/article.md",
        markdown=True,
    )
