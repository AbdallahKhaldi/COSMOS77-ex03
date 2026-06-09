"""Tests for the chapter-write + editor task builders (crewai.Task mocked)."""

from __future__ import annotations

from cosmos77_ex03.crew import tasks_write as tw
from cosmos77_ex03.crew.schemas import Chapter


def test_write_task_english(mocker):
    task = mocker.patch("cosmos77_ex03.crew.tasks_write.Task")
    ch = Chapter(index=1, title="Intro", brief="b", citation_keys=["k1"])
    tw.write_task("W", ch, "out")
    kwargs = task.call_args.kwargs
    assert kwargs["output_file"] == "out/chapters/ch_01.md"
    assert kwargs["async_execution"] is True
    assert kwargs["markdown"] is True
    assert "English" in kwargs["description"]
    assert "k1" in kwargs["description"]


def test_write_task_bidi_is_hebrew(mocker):
    task = mocker.patch("cosmos77_ex03.crew.tasks_write.Task")
    tw.write_task("W", Chapter(index=8, title="BiDi", is_bidi=True), "out")
    kwargs = task.call_args.kwargs
    assert "HEBREW" in kwargs["description"]
    assert kwargs["output_file"] == "out/chapters/ch_08.md"


def test_write_task_can_be_sync(mocker):
    task = mocker.patch("cosmos77_ex03.crew.tasks_write.Task")
    tw.write_task("W", Chapter(index=2, title="X"), "out", async_exec=False)
    assert task.call_args.kwargs["async_execution"] is False


def test_editor_task(mocker):
    task = mocker.patch("cosmos77_ex03.crew.tasks_write.Task")
    tw.editor_task("E", ["w1", "w2"], "out")
    kwargs = task.call_args.kwargs
    assert kwargs["context"] == ["w1", "w2"]
    assert kwargs["output_file"] == "out/article.md"
    assert kwargs["agent"] == "E"
