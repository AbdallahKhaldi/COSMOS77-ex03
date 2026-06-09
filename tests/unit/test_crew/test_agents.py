"""Tests for the agent factories (crewai.Agent + tools mocked)."""

from __future__ import annotations

from cosmos77_ex03.crew import agents


def test_skill_path_points_into_package():
    assert agents.skill_path("researcher").endswith("skills/researcher")


def test_make_agent_defaults(mocker):
    agent = mocker.patch.object(agents, "Agent")
    result = agents.make_agent(role="R", goal="G", backstory="B", llm="LLM")
    kwargs = agent.call_args.kwargs
    assert kwargs["allow_delegation"] is False
    assert kwargs["verbose"] is False
    assert kwargs["tools"] == [] and kwargs["skills"] == []
    assert result is agent.return_value


def test_builders_wire_role_skills_and_tools(mocker):
    mocker.patch.object(agents, "Agent", side_effect=lambda **k: k)
    mocker.patch.object(agents, "web_search_tools", return_value=["WS"])
    mocker.patch.object(agents, "file_writer_tools", return_value=["FW"])

    r = agents.researcher("LLM")
    assert "Research" in r["role"]
    assert r["skills"] == [agents.skill_path("researcher")]
    assert r["tools"] == ["WS"]

    la = agents.latex_author("LLM")
    assert la["skills"] == [agents.skill_path("latex-author")]
    assert la["tools"] == ["FW"]

    cw = agents.chapter_writer("LLM", index=3)
    assert "#3" in cw["role"]
    assert cw["skills"] == [agents.skill_path("technical-writer")]

    for builder in (agents.planner, agents.figure_agent, agents.bidi_writer, agents.editor):
        a = builder("LLM")
        assert a["skills"] == [agents.skill_path("technical-writer")]


def test_build_agents_returns_full_roster(mocker):
    mocker.patch.object(agents, "Agent", side_effect=lambda **k: k["role"])
    mocker.patch.object(agents, "web_search_tools", return_value=[])
    mocker.patch.object(agents, "file_writer_tools", return_value=[])
    mocker.patch("cosmos77_ex03.providers.factory.build_llm", return_value="LLM")
    roster = agents.build_agents(cfg=mocker.Mock())
    assert set(roster) == {
        "researcher",
        "planner",
        "figure_agent",
        "bidi_writer",
        "editor",
        "latex_author",
    }
