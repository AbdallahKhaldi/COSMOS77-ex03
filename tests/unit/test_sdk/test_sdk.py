"""Tests for the SDK skeleton (injected deps, NotImplementedError stubs)."""

from __future__ import annotations

import pytest

from cosmos77_ex03.sdk.sdk import SDK
from cosmos77_ex03.shared.gatekeeper import Gatekeeper


class _FakeConfig:
    def active_provider(self) -> str:
        return "gemini"

    def paths(self) -> dict:
        return {"figures_dir": "tex/figures"}


def test_sdk_uses_injected_deps():
    gk = Gatekeeper()
    sdk = SDK(config=_FakeConfig(), gatekeeper=gk)
    assert sdk.gatekeeper is gk


@pytest.mark.parametrize(
    "method",
    [
        "run",
        "build_pdf",
        "qa_pdf",
    ],
)
def test_stubs_raise_not_implemented(method):
    sdk = SDK(config=_FakeConfig(), gatekeeper=Gatekeeper())
    with pytest.raises(NotImplementedError):
        getattr(sdk, method)()


def test_spec_sheet_returns_dict():
    sdk = SDK(config=_FakeConfig(), gatekeeper=Gatekeeper())
    sheet = sdk.spec_sheet()
    assert isinstance(sheet, dict)
    assert sheet["provider"] == "gemini"


def test_sdk_default_construction():
    sdk = SDK()
    assert sdk.config.active_provider() == "gemini"
    assert isinstance(sdk.spec_sheet(), dict)


def test_smoke_records_usage_and_returns_text(mocker):
    fake_usage = {
        "prompt_tokens": 5,
        "completion_tokens": 2,
        "total_tokens": 7,
        "successful_requests": 1,
    }
    mocker.patch("cosmos77_ex03.crew.smoke.run_smoke", return_value=("pipeline-ok", fake_usage))
    gk = Gatekeeper()
    sdk = SDK(config=_FakeConfig(), gatekeeper=gk)
    assert sdk.smoke() == "pipeline-ok"
    assert gk.usage.total_tokens == 7


def test_build_agents_delegates(mocker):
    fake = {"researcher": object()}
    mocker.patch("cosmos77_ex03.crew.agents.build_agents", return_value=fake)
    sdk = SDK(config=_FakeConfig(), gatekeeper=Gatekeeper())
    assert sdk.build_agents() is fake


def test_research_delegates_and_records(mocker):
    from cosmos77_ex03.crew.schemas import Chapter, Outline

    outline = Outline(chapters=[Chapter(index=1, title="A")])
    mocker.patch(
        "cosmos77_ex03.crew.research_run.run_research",
        return_value=(outline, {"total_tokens": 9}),
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
    mocker.patch(
        "cosmos77_ex03.figures.charts.generate_all",
        return_value=["tex/figures/adoption.pdf", "tex/figures/frameworks.pdf"],
    )
    sdk = SDK(config=_FakeConfig(), gatekeeper=Gatekeeper())
    assert sdk.make_figures() == ["tex/figures/adoption.pdf", "tex/figures/frameworks.pdf"]


def test_assemble_latex_delegates(mocker):
    mocker.patch("cosmos77_ex03.latex.assemble.assemble", return_value={"sections": 12})
    sdk = SDK(config=_FakeConfig(), gatekeeper=Gatekeeper())
    assert sdk.assemble_latex() == {"sections": 12}
