"""Tests for the latex_author task builder (crewai.Task mocked)."""

from __future__ import annotations

from cosmos77_ex03.crew import tasks_latex as tl


def test_latex_author_task(mocker):
    task = mocker.patch("cosmos77_ex03.crew.tasks_latex.Task")
    tl.latex_author_task("LA", "## H\nbody", "out/sections/ch_01.tex")
    kwargs = task.call_args.kwargs
    assert kwargs["output_file"] == "out/sections/ch_01.tex"
    assert kwargs["agent"] == "LA"
    assert "ONLY LaTeX" in kwargs["description"]


def test_latex_author_task_hebrew(mocker):
    task = mocker.patch("cosmos77_ex03.crew.tasks_latex.Task")
    tl.latex_author_task("LA", "## עברית", "out.tex", hebrew=True)
    assert "foreignlanguage" in task.call_args.kwargs["description"]
