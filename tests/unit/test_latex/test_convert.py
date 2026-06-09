"""Tests for the deterministic Markdown -> LaTeX converter (B11, B8)."""

from __future__ import annotations

from cosmos77_ex03.latex.convert import md_to_latex


def test_heading_and_paragraph():
    out = md_to_latex("## Intro\n\nHello world \\cite{k1}.")
    assert "\\section{Intro}" in out
    assert "Hello world \\cite{k1}." in out


def test_inline_formatting_and_escaping():
    out = md_to_latex("Use **bold**, *italic*, `code`, 50% & more_data.")
    assert "\\textbf{bold}" in out
    assert "\\textit{italic}" in out
    assert "\\texttt{code}" in out
    assert "50\\%" in out and "\\&" in out and "more\\_data" in out


def test_cite_preserved_through_escaping():
    out = md_to_latex("See \\cite{a,b} for 100%.")
    assert "\\cite{a,b}" in out
    assert "100\\%" in out


def test_lists():
    out = md_to_latex("- one\n- two")
    assert "\\begin{itemize}" in out and "\\item one" in out


def test_code_fence_stripped():
    out = md_to_latex("```markdown\n## H\n\nbody\n```")
    assert "```" not in out and "\\section{H}" in out


def test_hebrew_wrapping():
    out = md_to_latex("## פרק\n\nשלום \\cite{k}", hebrew=True)
    assert out.startswith("\\selectlanguage{hebrew}")
    assert "\\selectlanguage{english}" in out
    assert "שלום" in out
