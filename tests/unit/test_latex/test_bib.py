"""Tests for refs.bib generation + cited-key extraction (B9)."""

from __future__ import annotations

from cosmos77_ex03.latex.bib import build_refs_bib, cited_keys


def test_cited_keys_extracts_multi():
    assert cited_keys(["text \\cite{a} more \\cite{b,c}"]) == {"a", "b", "c"}


def test_build_refs_bib_escapes_and_fills_missing():
    citations = [
        {
            "key": "segal2026",
            "author": "Segal",
            "title": "Arch & Agents",
            "year": "2026",
            "url": "http://x",
        }
    ]
    bib = build_refs_bib(citations, required_keys={"segal2026", "ghost"})
    assert "@misc{segal2026," in bib
    assert "Arch \\& Agents" in bib
    assert "\\url{http://x}" in bib
    assert "@misc{ghost," in bib  # cited-but-missing -> placeholder so it resolves
