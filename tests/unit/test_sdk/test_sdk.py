"""Tests for the SDK skeleton (injected deps, NotImplementedError stubs)."""

from __future__ import annotations

import pytest

from cosmos77_ex03.sdk.sdk import SDK
from cosmos77_ex03.shared.gatekeeper import Gatekeeper


class _FakeConfig:
    def active_provider(self) -> str:
        return "gemini"


def test_sdk_uses_injected_deps():
    gk = Gatekeeper()
    sdk = SDK(config=_FakeConfig(), gatekeeper=gk)
    assert sdk.gatekeeper is gk


@pytest.mark.parametrize(
    "method",
    [
        "run",
        "research",
        "write_chapters",
        "make_figures",
        "assemble_latex",
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
