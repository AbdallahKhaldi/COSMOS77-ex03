"""Tests for the Gatekeeper cost/usage meter (record, spec_sheet, scrub)."""

from __future__ import annotations

from cosmos77_ex03.shared.gatekeeper import Gatekeeper


class _FakeUsage:
    def __init__(self, prompt, completion, total, requests):
        self.prompt_tokens = prompt
        self.completion_tokens = completion
        self.total_tokens = total
        self.successful_requests = requests


def test_record_dict_accrues():
    g = Gatekeeper()
    g.record(
        {
            "prompt_tokens": 100,
            "completion_tokens": 50,
            "total_tokens": 150,
            "successful_requests": 1,
        }
    )
    g.record(
        {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15, "successful_requests": 1}
    )
    u = g.usage
    assert (u.prompt_tokens, u.completion_tokens, u.total_tokens, u.successful_requests) == (
        110,
        55,
        165,
        2,
    )


def test_record_object_with_total_fallback():
    g = Gatekeeper()
    g.record(_FakeUsage(40, 60, 0, 1))  # total 0 -> falls back to prompt+completion
    assert g.usage.total_tokens == 100


def test_record_none_is_noop():
    g = Gatekeeper()
    g.record(None)
    assert g.usage.total_tokens == 0


def test_estimate_cost_gemini_is_zero():
    g = Gatekeeper()
    g.record({"prompt_tokens": 1_000_000, "completion_tokens": 1_000_000})
    assert g.estimate_cost("gemini") == 0.0


def test_estimate_cost_groq_nonzero():
    g = Gatekeeper()
    g.record({"prompt_tokens": 1_000_000, "completion_tokens": 0})
    assert g.estimate_cost("groq") == 0.59


def test_estimate_cost_unknown_provider_is_zero():
    g = Gatekeeper()
    g.record({"prompt_tokens": 1_000_000})
    assert g.estimate_cost("mistral") == 0.0


def test_spec_sheet_shape():
    g = Gatekeeper()
    g.record(
        {"prompt_tokens": 10, "completion_tokens": 5, "total_tokens": 15, "successful_requests": 1}
    )
    s = g.spec_sheet(provider="gemini", wall_clock_s=1.5)
    assert s["prompt_tokens"] == 10
    assert s["provider"] == "gemini"
    assert s["estimated_cost_usd"] == 0.0
    assert s["wall_clock_s"] == 1.5
    for key in ("prompt_tokens", "completion_tokens", "total_tokens", "successful_requests"):
        assert key in s


def test_scrub_redacts_keys():
    out = Gatekeeper.scrub(
        "leak AQ.Ab8RN6K7ZXd7obc7AJSgnKhjP7USaSk and AIzaSyABCDEFGHIJKLMNOPQRSTUVWX12345678 end"
    )
    assert "AQ.Ab8" not in out
    assert "AIzaSy" not in out
    assert "[REDACTED]" in out
