"""Tests for the research runner (crew + agents mocked; artifacts persisted)."""

from __future__ import annotations

import json

from cosmos77_ex03.crew import research_run
from cosmos77_ex03.crew.schemas import Chapter, Citation, Outline


def _cfg(mocker, out_dir):
    cfg = mocker.Mock()
    cfg.paths.return_value = {"output_dir": out_dir, "reference_pdf": ""}
    cfg.get.side_effect = lambda key, default=None: {
        "crew.num_chapters": 2,
        "crew.max_rpm": 10,
    }.get(key, default)
    return cfg


def test_run_research_persists_and_returns(tmp_path, mocker):
    out_dir = str(tmp_path / "out")
    outline = Outline(
        chapters=[Chapter(index=1, title="A", is_bidi=True), Chapter(index=2, title="B")],
        citations=[Citation(key="segal2026", title="Arch 2026")],
    )
    mocker.patch.object(research_run, "build_llm", return_value="LLM")
    mocker.patch.object(research_run, "build_researcher", return_value="R")
    mocker.patch.object(research_run, "build_planner", return_value="P")
    mocker.patch.object(research_run, "research_task", return_value="RT")
    mocker.patch.object(research_run, "outline_task", return_value="OT")
    fake_result = mocker.Mock(pydantic=outline, token_usage={"total_tokens": 3})
    crew = mocker.Mock()
    crew.kickoff.return_value = fake_result
    mocker.patch.object(research_run, "Crew", return_value=crew)

    result_outline, usage = research_run.run_research(_cfg(mocker, out_dir))

    assert result_outline is outline
    assert usage == {"total_tokens": 3}
    oj = json.loads((tmp_path / "out" / "outline.json").read_text())
    assert len(oj["chapters"]) == 2
    cj = json.loads((tmp_path / "out" / "citations.json").read_text())
    assert cj[0]["key"] == "segal2026"
    assert "Hebrew BiDi" in (tmp_path / "out" / "outline.md").read_text()
