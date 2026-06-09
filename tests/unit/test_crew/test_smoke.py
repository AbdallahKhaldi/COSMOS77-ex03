"""Tests for the one-agent smoke crew (CrewAI fully mocked; no live call)."""

from __future__ import annotations

from cosmos77_ex03.crew import smoke


class _Result:
    def __init__(self, raw, token_usage):
        self.raw = raw
        self.token_usage = token_usage


def test_build_smoke_crew_wires_one_agent_and_task(mocker):
    mocker.patch.object(smoke, "build_llm", return_value="LLM")
    agent = mocker.patch.object(smoke, "Agent")
    task = mocker.patch.object(smoke, "Task")
    crew = mocker.patch.object(smoke, "Crew")
    result = smoke.build_smoke_crew(mocker.Mock())
    agent.assert_called_once()
    task.assert_called_once()
    crew.assert_called_once()
    assert result is crew.return_value


def test_run_smoke_returns_text_and_usage(mocker):
    fake_usage = {"total_tokens": 7}
    fake_crew = mocker.Mock()
    fake_crew.kickoff.return_value = _Result("pipeline-ok", fake_usage)
    mocker.patch.object(smoke, "build_smoke_crew", return_value=fake_crew)
    text, usage = smoke.run_smoke(cfg=mocker.Mock())
    assert text == "pipeline-ok"
    assert usage == fake_usage


def test_run_smoke_falls_back_to_str(mocker):
    class _R:
        raw = ""
        token_usage = None

        def __str__(self):
            return "fallback-text"

    fake_crew = mocker.Mock()
    fake_crew.kickoff.return_value = _R()
    mocker.patch.object(smoke, "build_smoke_crew", return_value=fake_crew)
    text, usage = smoke.run_smoke(cfg=mocker.Mock())
    assert text == "fallback-text"
    assert usage is None


def test_run_smoke_defaults_config_when_none(mocker):
    fake_crew = mocker.Mock()
    fake_crew.kickoff.return_value = _Result("ok", {"total_tokens": 1})
    mocker.patch.object(smoke, "build_smoke_crew", return_value=fake_crew)
    text, _ = smoke.run_smoke()  # cfg=None -> real Config() loaded, no live LLM call
    assert text == "ok"
