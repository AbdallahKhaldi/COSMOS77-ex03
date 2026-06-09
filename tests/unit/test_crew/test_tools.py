"""Tests for crew tool selection (crewai_tools mocked; env-driven fallback)."""

from __future__ import annotations

from cosmos77_ex03.crew import tools


def test_has_serper(monkeypatch):
    monkeypatch.delenv("SERPER_API_KEY", raising=False)
    assert tools.has_serper() is False
    monkeypatch.setenv("SERPER_API_KEY", "x")
    assert tools.has_serper() is True


def test_web_search_uses_serper_when_keyed(monkeypatch, mocker):
    monkeypatch.setenv("SERPER_API_KEY", "x")
    serper = mocker.patch("crewai_tools.SerperDevTool")
    result = tools.web_search_tools()
    serper.assert_called_once()
    assert result == [serper.return_value]


def test_web_search_falls_back_without_key(monkeypatch, mocker):
    monkeypatch.delenv("SERPER_API_KEY", raising=False)
    scrape = mocker.patch("crewai_tools.ScrapeWebsiteTool")
    result = tools.web_search_tools()
    scrape.assert_called_once()
    assert result == [scrape.return_value]


def test_file_writer_tools(mocker):
    fw = mocker.patch("crewai_tools.FileWriterTool")
    assert tools.file_writer_tools() == [fw.return_value]
