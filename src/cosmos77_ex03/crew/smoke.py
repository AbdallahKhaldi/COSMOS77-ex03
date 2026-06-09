"""Minimal one-agent Gemini smoke crew — proves the provider works end-to-end.

This is the smallest possible CrewAI run: a single agent with a single task that
must reply ``pipeline-ok``. Phase 3 uses it to confirm the free Gemini backend is
reachable and that ``result.token_usage`` is captured for the Spec Sheet. Unit
tests mock CrewAI entirely; only the manual verification makes a live call.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from crewai import Agent, Crew, Process, Task

from cosmos77_ex03.providers.factory import build_llm

if TYPE_CHECKING:
    from cosmos77_ex03.shared.config import Config


def build_smoke_crew(cfg: Config) -> Crew:
    """Build a one-agent, one-task crew that must reply ``pipeline-ok``."""
    llm = build_llm(cfg)
    agent = Agent(
        role="Pipeline Smoke Tester",
        goal="Confirm the configured LLM backend is reachable.",
        backstory="You verify connectivity with a single, deterministic reply.",
        llm=llm,
        allow_delegation=False,
        verbose=False,
    )
    task = Task(
        description="Reply with exactly this text and nothing else: pipeline-ok",
        expected_output="The exact text: pipeline-ok",
        agent=agent,
    )
    return Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False)


def run_smoke(cfg: Config | None = None) -> tuple[str, Any]:
    """Run the smoke crew; return ``(reply_text, token_usage)``.

    ``token_usage`` is the CrewAI ``UsageMetrics`` (or ``None``) so the caller can
    feed it to the gatekeeper cost meter.
    """
    if cfg is None:
        from cosmos77_ex03.shared.config import Config

        cfg = Config()
    result = build_smoke_crew(cfg).kickoff()
    text = getattr(result, "raw", "") or str(result)
    usage = getattr(result, "token_usage", None)
    return text, usage
