"""Config-driven LLM provider factory (B12, ADR-005).

Reads ``config/providers.json`` via :class:`Config`, resolves the active
provider's model and ``api_key_env``, and builds a CrewAI ``LLM``. The model id
is never hardcoded — swap providers by editing config, not code.
"""

from __future__ import annotations

import os
from typing import TYPE_CHECKING

from crewai import LLM

from cosmos77_ex03.providers.registry import default_model, known_providers

if TYPE_CHECKING:
    from cosmos77_ex03.shared.config import Config


def resolve_model(cfg: Config, provider: str | None = None) -> str:
    """Return the model id for the (active) provider from config, else its default."""
    name = provider or cfg.active_provider()
    pcfg = cfg.provider_config(name)
    return str(pcfg.get("model") or default_model(name))


def resolve_api_key(cfg: Config, provider: str | None = None) -> str:
    """Return the API key for the provider from its ``api_key_env``; raise if missing."""
    name = provider or cfg.active_provider()
    pcfg = cfg.provider_config(name)
    env_var = pcfg.get("api_key_env")
    if not env_var:
        raise ValueError(f"provider {name!r} has no 'api_key_env' in providers.json")
    key = os.environ.get(env_var)
    if not key:
        raise ValueError(
            f"environment variable {env_var!r} is not set — put the {name} key in .env "
            "(see .env.example). The model is selected by config, never hardcoded."
        )
    return key


def build_llm(cfg: Config, provider: str | None = None) -> LLM:
    """Build a CrewAI ``LLM`` for the active (or named) provider from config (B12)."""
    name = provider or cfg.active_provider()
    if name not in known_providers():
        raise KeyError(f"unknown provider {name!r}; known: {sorted(known_providers())}")
    model = resolve_model(cfg, name)
    api_key = resolve_api_key(cfg, name)
    return LLM(model=model, api_key=api_key)
