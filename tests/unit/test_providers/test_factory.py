"""Tests for the LLM provider factory (crewai.LLM + os.environ mocked)."""

from __future__ import annotations

import json

import pytest

from cosmos77_ex03.providers import factory
from cosmos77_ex03.shared.config import Config


@pytest.fixture
def cfg(tmp_path):
    cdir = tmp_path / "config"
    cdir.mkdir()
    (cdir / "setup.json").write_text(json.dumps({"version": "1.00"}))
    (cdir / "providers.json").write_text(
        json.dumps(
            {
                "version": "1.00",
                "active": "gemini",
                "providers": {
                    "gemini": {"model": "gemini/gemini-2.5-flash", "api_key_env": "GEMINI_API_KEY"},
                    "groq": {
                        "model": "groq/llama-3.3-70b-versatile",
                        "api_key_env": "GROQ_API_KEY",
                    },
                    "openai": {"model": "gpt-4o", "api_key_env": "OPENAI_API_KEY"},
                    "noenv": {"model": "x/y"},
                },
            }
        )
    )
    return Config(cdir)


def test_resolve_model_from_config(cfg):
    assert factory.resolve_model(cfg) == "gemini/gemini-2.5-flash"
    assert factory.resolve_model(cfg, "groq") == "groq/llama-3.3-70b-versatile"


def test_build_llm_gemini(cfg, monkeypatch, mocker):
    monkeypatch.setenv("GEMINI_API_KEY", "k-gemini")
    fake = mocker.patch.object(factory, "LLM")
    llm = factory.build_llm(cfg)
    fake.assert_called_once_with(model="gemini/gemini-2.5-flash", api_key="k-gemini")
    assert llm is fake.return_value


def test_build_llm_groq(cfg, monkeypatch, mocker):
    monkeypatch.setenv("GROQ_API_KEY", "k-groq")
    fake = mocker.patch.object(factory, "LLM")
    factory.build_llm(cfg, "groq")
    fake.assert_called_once_with(model="groq/llama-3.3-70b-versatile", api_key="k-groq")


def test_build_llm_openai(cfg, monkeypatch, mocker):
    monkeypatch.setenv("OPENAI_API_KEY", "k-oai")
    fake = mocker.patch.object(factory, "LLM")
    factory.build_llm(cfg, "openai")
    fake.assert_called_once_with(model="gpt-4o", api_key="k-oai")


def test_build_llm_missing_key_raises(cfg, monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    with pytest.raises(ValueError, match="is not set"):
        factory.build_llm(cfg)


def test_build_llm_unknown_provider_raises(cfg):
    with pytest.raises(KeyError):
        factory.build_llm(cfg, "mistral")


def test_resolve_api_key_no_env_var_raises(cfg):
    with pytest.raises(ValueError, match="no 'api_key_env'"):
        factory.resolve_api_key(cfg, "noenv")
