"""Tests for the JSON + .env Config loader (dot-path, sections, providers)."""

from __future__ import annotations

import json

import pytest

from cosmos77_ex03.shared.config import Config


def _write_config(cdir, *, setup=None, providers=None):
    cdir.mkdir(exist_ok=True)
    (cdir / "setup.json").write_text(
        json.dumps(setup if setup is not None else {"version": "1.00"})
    )
    (cdir / "providers.json").write_text(
        json.dumps(
            providers
            if providers is not None
            else {"version": "1.00", "active": "gemini", "providers": {}}
        )
    )


@pytest.fixture
def cfg(tmp_path):
    cdir = tmp_path / "config"
    _write_config(
        cdir,
        setup={
            "version": "1.00",
            "article": {"title": "T", "language_primary": "english", "target_pages": 15},
            "crew": {"process": "sequential", "num_chapters": 12, "max_rpm": 10},
            "paths": {"output_dir": "output", "tex_dir": "tex"},
        },
        providers={
            "version": "1.00",
            "active": "gemini",
            "providers": {
                "gemini": {"model": "gemini/gemini-2.5-flash", "api_key_env": "GEMINI_API_KEY"},
                "groq": {"model": "groq/llama-3.3-70b-versatile", "api_key_env": "GROQ_API_KEY"},
            },
        },
    )
    return Config(cdir)


def test_dot_path_get(cfg):
    assert cfg.get("crew.num_chapters") == 12
    assert cfg.get("article.target_pages") == 15


def test_get_missing_with_default(cfg):
    assert cfg.get("crew.nope", default=7) == 7


def test_get_missing_raises(cfg):
    with pytest.raises(KeyError):
        cfg.get("crew.nope")


def test_sections(cfg):
    assert cfg.article()["title"] == "T"
    assert cfg.crew()["process"] == "sequential"
    assert cfg.paths()["tex_dir"] == "tex"


def test_active_provider_and_config(cfg):
    assert cfg.active_provider() == "gemini"
    assert cfg.provider_config()["model"] == "gemini/gemini-2.5-flash"
    assert cfg.provider_config("groq")["api_key_env"] == "GROQ_API_KEY"


def test_unknown_provider_raises(cfg):
    with pytest.raises(KeyError):
        cfg.provider_config("mistral")


def test_env_reads_environ(cfg, monkeypatch):
    monkeypatch.setenv("FOO_BAR", "baz")
    assert cfg.env("FOO_BAR") == "baz"
    assert cfg.env("MISSING_X", "d") == "d"


def test_version_property_repr_and_providers(cfg):
    assert cfg.version == "1.00"
    assert "Config(" in repr(cfg)
    assert cfg.config_dir.name == "config"
    assert "gemini" in cfg.providers()["providers"]


def test_from_path(cfg):
    assert Config.from_path(cfg.config_dir).active_provider() == "gemini"


def test_missing_setup_raises(tmp_path):
    empty = tmp_path / "config"
    empty.mkdir()
    with pytest.raises(FileNotFoundError):
        Config(empty)


def test_version_mismatch_raises(tmp_path):
    cdir = tmp_path / "config"
    _write_config(cdir, setup={"version": "0.1"})
    with pytest.raises(ValueError, match="does not match"):
        Config(cdir)


def test_non_dict_json_raises(tmp_path):
    cdir = tmp_path / "config"
    cdir.mkdir()
    (cdir / "setup.json").write_text(json.dumps([1, 2, 3]))
    (cdir / "providers.json").write_text(json.dumps({"active": "x", "providers": {}}))
    with pytest.raises(ValueError, match="JSON object"):
        Config(cdir)
