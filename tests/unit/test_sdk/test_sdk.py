"""Tests for the SDK facade (injected deps + per-stage delegation)."""

from __future__ import annotations

from cosmos77_ex03.sdk.sdk import SDK
from cosmos77_ex03.shared.gatekeeper import Gatekeeper


class _FakeConfig:
    def active_provider(self) -> str:
        return "gemini"

    def paths(self) -> dict:
        return {"figures_dir": "tex/figures", "tex_dir": "tex"}

    def get(self, key, default=None):
        return default


def _sdk() -> SDK:
    return SDK(config=_FakeConfig(), gatekeeper=Gatekeeper())


def test_sdk_uses_injected_deps():
    gk = Gatekeeper()
    assert SDK(config=_FakeConfig(), gatekeeper=gk).gatekeeper is gk


def test_spec_sheet_returns_dict():
    sheet = _sdk().spec_sheet()
    assert isinstance(sheet, dict) and sheet["provider"] == "gemini"


def test_write_spec_sheet(tmp_path):
    import json
    from pathlib import Path

    out = _sdk().write_spec_sheet(str(tmp_path / "spec.json"))
    data = json.loads(Path(out).read_text(encoding="utf-8"))
    assert data["provider"] == "gemini" and "total_tokens" in data


def test_sdk_default_construction():
    sdk = SDK()
    assert sdk.config.active_provider() == "gemini"
    assert isinstance(sdk.spec_sheet(), dict)


def test_smoke_records_usage_and_returns_text(mocker):
    usage = {
        "prompt_tokens": 5,
        "completion_tokens": 2,
        "total_tokens": 7,
        "successful_requests": 1,
    }
    mocker.patch("cosmos77_ex03.crew.smoke.run_smoke", return_value=("pipeline-ok", usage))
    gk = Gatekeeper()
    sdk = SDK(config=_FakeConfig(), gatekeeper=gk)
    assert sdk.smoke() == "pipeline-ok"
    assert gk.usage.total_tokens == 7


def test_build_agents_delegates(mocker):
    fake = {"researcher": object()}
    mocker.patch("cosmos77_ex03.crew.agents.build_agents", return_value=fake)
    assert _sdk().build_agents() is fake


def test_research_delegates_and_records(mocker):
    from cosmos77_ex03.crew.schemas import Chapter, Outline

    outline = Outline(chapters=[Chapter(index=1, title="A")])
    mocker.patch(
        "cosmos77_ex03.crew.research_run.run_research", return_value=(outline, {"total_tokens": 9})
    )
    gk = Gatekeeper()
    sdk = SDK(config=_FakeConfig(), gatekeeper=gk)
    assert sdk.research() is outline
    assert gk.usage.total_tokens == 9


def test_write_chapters_delegates_and_records(mocker):
    mocker.patch("cosmos77_ex03.crew.write_run.run_write", return_value=(12, {"total_tokens": 12}))
    gk = Gatekeeper()
    sdk = SDK(config=_FakeConfig(), gatekeeper=gk)
    assert sdk.write_chapters() == 12
    assert gk.usage.total_tokens == 12


def test_make_figures_delegates(mocker):
    mocker.patch("cosmos77_ex03.figures.charts.generate_all", return_value=["a.pdf", "b.pdf"])
    assert _sdk().make_figures() == ["a.pdf", "b.pdf"]


def test_assemble_latex_delegates(mocker):
    mocker.patch("cosmos77_ex03.latex.assemble.assemble", return_value={"sections": 12})
    assert _sdk().assemble_latex() == {"sections": 12}


def test_build_pdf_delegates(mocker):
    run = mocker.patch("subprocess.run")
    result = _sdk().build_pdf()
    run.assert_called_once()
    assert result.endswith("main.pdf")


def test_qa_pdf_returns_report(mocker):
    from cosmos77_ex03.latex.qa import Check

    mocker.patch("cosmos77_ex03.latex.qa.run_checks", return_value=[Check("x", True, True, "")])
    result = _sdk().qa_pdf()
    assert result["ok"] is True and "x" in result["report"]


def test_run_chains_pipeline(mocker):
    sdk = _sdk()
    calls: list[str] = []
    for name in ("research", "write_chapters", "make_figures", "assemble_latex", "build_pdf"):
        mocker.patch.object(sdk, name, side_effect=lambda n=name: calls.append(n))
    mocker.patch.object(sdk, "qa_pdf", return_value={"ok": True, "report": "R"})
    result = sdk.run()
    assert calls == ["research", "write_chapters", "make_figures", "assemble_latex", "build_pdf"]
    assert result == {"ok": True, "report": "R"}
