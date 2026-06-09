"""Tests for the chapter-write runner (crew + agents mocked; BiDi routing)."""

from __future__ import annotations

from pathlib import Path

from cosmos77_ex03.crew import write_run
from cosmos77_ex03.crew.schemas import Chapter, Outline


def _cfg(mocker, out_dir, parallel=True):
    cfg = mocker.Mock()
    cfg.paths.return_value = {"output_dir": out_dir}
    cfg.get.side_effect = lambda key, default=None: {
        "crew.parallel_writers": parallel,
        "crew.max_rpm": 10,
    }.get(key, default)
    return cfg


def test_run_write_routes_bidi_and_stitches(tmp_path, mocker):
    out_dir = str(tmp_path / "out")
    chapters = Path(out_dir, "chapters")
    chapters.mkdir(parents=True)
    (chapters / "ch_01.md").write_text("## A\nbody A \\cite{k}", encoding="utf-8")
    (chapters / "ch_02.md").write_text("## B\nשלום עולם \\cite{k}", encoding="utf-8")
    outline = Outline(
        chapters=[Chapter(index=1, title="A"), Chapter(index=2, title="B", is_bidi=True)]
    )
    Path(out_dir, "outline.json").write_text(outline.model_dump_json(), encoding="utf-8")

    mocker.patch.object(write_run, "build_llm", return_value="LLM")
    cw = mocker.patch.object(write_run, "build_chapter_writer", return_value="CW")
    bw = mocker.patch.object(write_run, "build_bidi_writer", return_value="BW")
    mocker.patch.object(write_run, "build_editor", return_value="ED")
    mocker.patch.object(write_run, "write_task", side_effect=lambda *a, **k: f"WT{a[1].index}")
    mocker.patch.object(write_run, "editor_task", return_value="ET")
    crew = mocker.Mock()
    crew.kickoff.return_value = mocker.Mock(token_usage={"total_tokens": 5})
    mocker.patch.object(write_run, "Crew", return_value=crew)

    count, usage = write_run.run_write(_cfg(mocker, out_dir))

    assert count == 2
    assert usage == {"total_tokens": 5}
    bw.assert_called_once()  # exactly the BiDi chapter routes to bidi_writer
    assert cw.call_count == 1  # the non-BiDi chapter
    article = Path(out_dir, "article.md").read_text(encoding="utf-8")
    assert "body A" in article and "שלום" in article  # deterministic stitch fallback
