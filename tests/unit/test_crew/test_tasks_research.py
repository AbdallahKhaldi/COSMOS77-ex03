"""Tests for the research + outline task builders (crewai.Task mocked)."""

from __future__ import annotations

from cosmos77_ex03.crew import tasks_research as tr
from cosmos77_ex03.crew.schemas import Outline


def test_reference_excerpt_missing_returns_empty(tmp_path):
    assert tr.reference_excerpt(tmp_path / "nope.pdf") == ""


def test_reference_excerpt_extracts_and_truncates(tmp_path, mocker):
    f = tmp_path / "r.pdf"
    f.write_text("x")
    page = mocker.Mock()
    page.extract_text.return_value = "Hello world"
    fake_pdf = mocker.MagicMock()
    fake_pdf.pages = [page, page]
    fake_pdf.__enter__.return_value = fake_pdf
    mocker.patch("pdfplumber.open", return_value=fake_pdf)
    assert tr.reference_excerpt(f, max_chars=5) == "Hello"


def test_reference_excerpt_handles_error(tmp_path, mocker):
    f = tmp_path / "r.pdf"
    f.write_text("x")
    mocker.patch("pdfplumber.open", side_effect=RuntimeError("bad"))
    assert tr.reference_excerpt(f) == ""


def test_research_task_builds(mocker):
    task = mocker.patch("cosmos77_ex03.crew.tasks_research.Task")
    mocker.patch.object(tr, "reference_excerpt", return_value="")
    tr.research_task("AGENT", "outdir")
    kwargs = task.call_args.kwargs
    assert kwargs["output_file"] == "outdir/research.md"
    assert kwargs["agent"] == "AGENT"
    assert "Sources" in kwargs["expected_output"]


def test_outline_task_builds(mocker):
    task = mocker.patch("cosmos77_ex03.crew.tasks_research.Task")
    tr.outline_task("PLANNER", ["ctx"], 12)
    kwargs = task.call_args.kwargs
    assert kwargs["output_pydantic"] is Outline
    assert kwargs["context"] == ["ctx"]
    assert "12" in kwargs["description"]
    assert kwargs["agent"] == "PLANNER"
