# Prompt log 002 — Phase 2: Shared infrastructure + provider factory

**Phase:** 2 — Shared layer port + the config-driven LLM provider factory (B12)
**Authors:** Abdallah Khaldi, Tasneem Natour
**Date:** 2026-06-09

## Prompt issued

> Phase 2 goal: port the proven shared layer from HW2 and build the
> config-driven LLM provider factory (B12). All TDD; LLM calls mocked. Port
> `version.py`, `config.py` (dot-path loader + `.env`), `logging_setup.py`, and
> REPURPOSE `gatekeeper.py` as a cost/usage METER (no hard cap): `record(token_usage)`,
> `estimate_cost(provider)`, `spec_sheet()`, `scrub()`. New: `providers/factory.py`
> (`build_llm(cfg) -> crewai.LLM`), `providers/registry.py`, and the `SDK` skeleton
> with `NotImplementedError` stubs. Mock `os.environ` + `crewai.LLM`.

## What was done (direct construction — interdependent TDD layer)

- **`shared/version.py`** — `VERSION="1.00"` + `validate_config_version` (exact match).
- **`shared/config.py`** — `Config` loads `setup.json` + `providers.json`, version-checks,
  loads `.env`; dot-path `get()`, section accessors (`article/crew/paths/providers`),
  `active_provider()` + `provider_config()`.
- **`shared/logging_setup.py`** — `init_logging` (dictConfig + dir creation) + `get_logger`
  under the `cosmos77_ex03` namespace.
- **`shared/gatekeeper.py`** — repurposed as a token/usage METER: `record()` accrues
  prompt/completion/total tokens + successful_requests (dict OR CrewAI `UsageMetrics`),
  `estimate_cost(provider)` (Gemini free = 0, others from a rate table), `spec_sheet()`,
  and `scrub()` (redacts `AIza…`/`AQ.…`/`sk-…`/`gh*_…`/`Bearer …`).
- **`constants.py`** — added `AGENT_ROLES`, `CHAPTER_STATUSES` (kept `DEFAULT_ENCODING` etc).
- **`providers/registry.py`** — known providers + fallback default models; unknown raises.
- **`providers/factory.py`** — `build_llm(cfg)` resolves model + key from config, raises a
  clear error if the key env var is missing; provider-agnostic, never hardcodes the model.
- **`sdk/sdk.py`** — `SDK` facade wiring `Config` + `Gatekeeper`; `run/smoke/research/
  write_chapters/make_figures/assemble_latex/build_pdf/qa_pdf` stubs raise
  `NotImplementedError`; `spec_sheet()` already returns the gatekeeper aggregate.

## Verification

```bash
uv run ruff check .                 # zero
uv run python scripts/check_line_cap.py   # 0 offenders
uv run pytest -m "not live"         # 51 passed, coverage 100%
```

All Phase-2 modules report **100% coverage** (overall gate ≥85%). The 51 tests
mock `os.environ` + `crewai.LLM`; no live LLM call in the suite (rule 6).
