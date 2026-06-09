"""Provider registry — known LLM providers and their default model ids.

The active provider and per-provider model live in ``config/providers.json``;
this registry supplies a fallback default model and validates provider names so
an unknown provider fails fast (rule 4: no hardcoded model in business logic).
"""

from __future__ import annotations

#: Fallback default model per provider — used only if providers.json omits ``model``.
PROVIDER_DEFAULTS: dict[str, str] = {
    "gemini": "gemini/gemini-2.5-flash",
    "groq": "groq/llama-3.3-70b-versatile",
    "openai": "gpt-4o",
}


def known_providers() -> tuple[str, ...]:
    """Return the tuple of registered provider names."""
    return tuple(PROVIDER_DEFAULTS)


def default_model(provider: str) -> str:
    """Return the fallback default model id for ``provider``; raise if unknown."""
    if provider not in PROVIDER_DEFAULTS:
        raise KeyError(f"unknown provider {provider!r}; known: {sorted(PROVIDER_DEFAULTS)}")
    return PROVIDER_DEFAULTS[provider]
