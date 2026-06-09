"""Tests for main.tex assembly (B2 cover, B3 TOC, visuals interleaved)."""

from __future__ import annotations

from cosmos77_ex03.latex.document import build_main_tex


def test_main_tex_structure():
    article = {
        "title": "AI & Agents",
        "author": "A and B",
        "course": "203.3763",
        "instructor": "Dr. Segal",
    }
    out = build_main_tex(article, [1, 2, 8, 12])
    assert "\\input{preamble.tex}" in out
    assert "\\begin{document}" in out and "\\end{document}" in out
    assert "AI \\& Agents" in out  # cover title escaped
    assert "\\tableofcontents" in out
    for i in (1, 2, 8, 12):
        assert f"\\input{{sections/ch_{i:02d}.tex}}" in out
    assert "\\input{diagram.tex}" in out
    assert "adoption.pdf" in out and "frameworks.pdf" in out
    assert "\\input{table.tex}" in out and "\\input{formula.tex}" in out
    assert "\\printbibliography" in out
