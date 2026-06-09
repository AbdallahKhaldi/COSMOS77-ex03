"""Tests for the provider registry (known providers + default models)."""

from __future__ import annotations

import pytest

from cosmos77_ex03.providers.registry import default_model, known_providers


def test_known_providers():
    assert set(known_providers()) == {"gemini", "groq", "openai"}


def test_default_model():
    assert default_model("gemini") == "gemini/gemini-2.5-flash"
    assert default_model("openai") == "gpt-4o"


def test_default_model_unknown_raises():
    with pytest.raises(KeyError):
        default_model("mistral")
