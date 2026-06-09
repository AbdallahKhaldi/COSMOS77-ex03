"""Gatekeeper — token-usage + cost METER for the Spec Sheet (CLAUDE.md rule 13).

Repurposed from HW2's budget gate: there is NO hard cap (Gemini free tier), but
every LLM call's token usage is recorded so the Spec Sheet (B12) can report
tokens, request counts, and an estimated cost. :meth:`scrub` redacts secrets
before anything is logged (the cyber layer).
"""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import asdict, dataclass
from typing import Any

#: Indicative USD cost per 1M tokens (prompt, completion). Gemini free tier = 0.
DEFAULT_RATES: dict[str, tuple[float, float]] = {
    "gemini": (0.0, 0.0),
    "groq": (0.59, 0.79),
    "openai": (2.5, 10.0),
}

_SECRET_RE = re.compile(
    r"(AIza[0-9A-Za-z_\-]{20,}|AQ\.[A-Za-z0-9_\-]{12,}|sk-[A-Za-z0-9_\-]{6,}"
    r"|gh[pousr]_[A-Za-z0-9]{16,}|Bearer\s+[A-Za-z0-9._\-]+)"
)


@dataclass
class Usage:
    """Running token / request totals across every metered LLM call."""

    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    successful_requests: int = 0


class Gatekeeper:
    """Accumulates CrewAI token usage and produces the Spec Sheet (no hard cap)."""

    def __init__(self) -> None:
        self._usage = Usage()

    @property
    def usage(self) -> Usage:
        """The live usage counters."""
        return self._usage

    @staticmethod
    def _field(src: Any, name: str) -> int:
        if isinstance(src, Mapping):
            return int(src.get(name, 0) or 0)
        return int(getattr(src, name, 0) or 0)

    def record(self, token_usage: Any) -> None:
        """Accumulate one call's usage (a dict or a CrewAI ``UsageMetrics`` object)."""
        if token_usage is None:
            return
        prompt = self._field(token_usage, "prompt_tokens")
        completion = self._field(token_usage, "completion_tokens")
        total = self._field(token_usage, "total_tokens") or (prompt + completion)
        self._usage.prompt_tokens += prompt
        self._usage.completion_tokens += completion
        self._usage.total_tokens += total
        self._usage.successful_requests += self._field(token_usage, "successful_requests")

    def estimate_cost(
        self, provider: str, rates: Mapping[str, tuple[float, float]] | None = None
    ) -> float:
        """Estimate USD cost from accumulated tokens for ``provider`` (Gemini = 0)."""
        rate_in, rate_out = (rates or DEFAULT_RATES).get(provider, (0.0, 0.0))
        cost = (self._usage.prompt_tokens / 1_000_000) * rate_in
        cost += (self._usage.completion_tokens / 1_000_000) * rate_out
        return round(cost, 6)

    def spec_sheet(self, provider: str = "gemini", **extra: Any) -> dict[str, Any]:
        """Return the aggregate Spec Sheet (tokens, requests, est. cost, + extras)."""
        sheet = asdict(self._usage)
        sheet["provider"] = provider
        sheet["estimated_cost_usd"] = self.estimate_cost(provider)
        sheet.update(extra)
        return sheet

    @staticmethod
    def scrub(text: str) -> str:
        """Redact anything resembling an API key/token before logging."""
        return _SECRET_RE.sub("[REDACTED]", text)
