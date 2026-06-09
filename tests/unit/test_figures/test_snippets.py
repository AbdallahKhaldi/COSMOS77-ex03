"""Content checks on the committed LaTeX snippets (B4 image, B6 table, B7 formula)."""

from __future__ import annotations

from pathlib import Path

_TEX = Path(__file__).resolve().parents[3] / "tex"


def test_table_uses_tabularx_and_booktabs_no_hline():
    text = (_TEX / "table.tex").read_text(encoding="utf-8")
    assert "tabularx" in text
    assert "\\toprule" in text and "\\bottomrule" in text
    assert "\\hline" not in text  # hline risks overflow; booktabs only


def test_formula_is_a_display_equation():
    text = (_TEX / "formula.tex").read_text(encoding="utf-8")
    assert "\\begin{equation}" in text
    assert "\\underbrace" in text  # genuinely "fancy", not flat text


def test_diagram_is_tikz_with_caption():
    text = (_TEX / "diagram.tex").read_text(encoding="utf-8")
    assert "tikzpicture" in text
    assert "\\caption" in text and "\\label{fig:arch}" in text
