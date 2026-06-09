"""Tests for the §13.1 PDF QA checklist validator (B15)."""

from __future__ import annotations

from pathlib import Path

from cosmos77_ex03.latex import qa


def _make_project(tmp_path, *, with_table=True):
    d = tmp_path / "tex"
    (d / "sections").mkdir(parents=True)
    (d / "figures").mkdir()
    (d / "preamble.tex").write_text("\\fancyhead[R]{\\thepage}\n", encoding="utf-8")
    table = "\\begin{tabularx}{\\linewidth}{lXr}\\end{tabularx}" if with_table else ""
    (d / "main.tex").write_text(
        "\\tableofcontents\n\\includegraphics{figures/a.pdf}\n"
        "\\begin{equation}E=mc^2\\end{equation}\n" + table + "\n\\cite{k}\n",
        encoding="utf-8",
    )
    (d / "sections" / "ch_08.tex").write_text(
        "\\selectlanguage{hebrew}\nשלום עולם\n", encoding="utf-8"
    )
    (d / "figures" / "a.pdf").write_bytes(b"%PDF-1.4 fake")
    (d / "main.pdf").write_bytes(b"%PDF-1.4 fake")
    (d / "main.bbl").write_text("\\entry{k}{misc}{}", encoding="utf-8")
    (d / "main.log").write_text("no warnings here", encoding="utf-8")
    (d / "main.out").write_text("\\BOOKMARK", encoding="utf-8")
    return d


def test_run_checks_all_critical_pass(tmp_path, mocker):
    mocker.patch("cosmos77_ex03.latex.qa.page_count", return_value=15)
    checks = qa.run_checks(_make_project(tmp_path, with_table=True))
    assert not qa.has_critical_failure(checks)
    by_name = {c.name: c.ok for c in checks}
    assert by_name["B8 Hebrew BiDi chapter"]
    assert by_name["B9 citations + .bbl"]


def test_run_checks_fails_without_table(tmp_path, mocker):
    mocker.patch("cosmos77_ex03.latex.qa.page_count", return_value=15)
    checks = qa.run_checks(_make_project(tmp_path, with_table=False))
    assert qa.has_critical_failure(checks)
    assert "CRITICAL FAILURE" in qa.format_report(checks)


def test_page_count_real_and_missing():
    real = Path("tex/figures/adoption.pdf")
    if real.exists():
        assert qa.page_count(real) >= 1
    assert qa.page_count(Path("does-not-exist.pdf")) == 0
