"""CrewAI tool selection (web search + file writing).

Web search uses ``SerperDevTool`` when ``SERPER_API_KEY`` is set; otherwise it
falls back to a keyless ``ScrapeWebsiteTool``. ``WebsiteSearchTool`` is
intentionally omitted — it needs a RAG embedding backend we do not provision on
the free tier. The local 2026 reference PDF is grounded as task *context* in
Phase 5 (more robust than a RAG PDF tool). ``FileWriterTool`` writes artifacts.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

#: The primary local source the researcher grounds on (injected as context).
REFERENCE_PDF = Path(__file__).resolve().parents[3] / "reference" / "Agent_Architecture_2026.pdf"


def has_serper() -> bool:
    """Return True when a Serper API key is configured (enables SerperDevTool)."""
    return bool(os.environ.get("SERPER_API_KEY"))


def web_search_tools() -> list[Any]:
    """Return the web-search tool set: Serper if keyed, else a keyless scraper."""
    if has_serper():
        from crewai_tools import SerperDevTool

        return [SerperDevTool()]
    from crewai_tools import ScrapeWebsiteTool

    return [ScrapeWebsiteTool()]


def file_writer_tools() -> list[Any]:
    """Return a FileWriterTool for writing .md/.tex outputs."""
    from crewai_tools import FileWriterTool

    return [FileWriterTool()]
