"""Pydantic schemas for structured crew outputs (the outline + citations).

CrewAI populates ``Task.output.pydantic`` against these models, giving us a
validated, machine-readable ``outline.json`` / ``citations.json`` instead of
parsing free-form LLM text.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class Citation(BaseModel):
    """A BibTeX-ready source record (drives ``refs.bib`` in Phase 8)."""

    key: str
    author: str = ""
    title: str = ""
    year: str = ""
    venue: str = ""
    url: str = ""


class Chapter(BaseModel):
    """One planned chapter; exactly one chapter sets ``is_bidi=True`` (B8)."""

    index: int
    title: str
    brief: str = ""
    citation_keys: list[str] = Field(default_factory=list)
    is_bidi: bool = False


class Outline(BaseModel):
    """The full article plan: ordered chapters + the citation pool."""

    chapters: list[Chapter]
    citations: list[Citation] = Field(default_factory=list)
