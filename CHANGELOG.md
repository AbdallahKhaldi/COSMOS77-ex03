# Changelog

All notable changes to COSMOS77-ex03 are documented here. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); the project adheres to
a single `1.00` version line tagged at submission (CLAUDE.md rule 10).

## [1.00] — in progress

### Phase 0 — Repo bootstrap
- Scaffolded the `src/cosmos77_ex03` package, `tests/`, `docs/`, `config/`,
  `scripts/`, and the `tex/` LaTeX-project directory.
- Added `pyproject.toml` (uv-managed, Python 3.11, CrewAI + matplotlib stack),
  ruff / coverage / pytest configuration, and the 150-line-cap checker.
- Added `CLAUDE.md` (the 17 binding rules), `LICENSE` (MIT), `CONTRIBUTING.md`.
- Added `config/setup.json`, `config/providers.json` (provider-agnostic LLM
  config), and `config/logging_config.json`.
- Wired pre-commit hooks and the GitHub Actions CI pipeline (ruff, line-cap,
  pytest with an 85% coverage gate; live LLM/LaTeX tests excluded).

### Phase 1 — Mandatory documentation
- `docs/PRD.md` — the whole assignment: context, stakeholders, user stories,
  15 functional requirements mapped to B1–B15, non-functional requirements,
  KPIs, and out-of-scope.
- 10 per-mechanism PRDs (`docs/PRD_*.md`): LLM provider factory, crew design,
  Skills, research tooling, figure generation, LaTeX template, BiDi chapter,
  PDF QA, Spec Sheet, and extension points.
- `docs/PLAN.md` — C4 model (Context/Container/Component/Code Mermaid), an
  end-to-end run sequence diagram, ADR-001..ADR-007, and a risk register.
- `docs/TODO.md` — 651 granular `T-NNNN | phase | area | description | DoD |
  status` items spanning P0–P12.

### Phase 2 — Shared infrastructure + provider factory
- `shared/version.py`, `shared/config.py` (dot-path JSON + `.env` loader),
  `shared/logging_setup.py`, and `shared/gatekeeper.py` repurposed as a
  token-usage / cost meter feeding the Spec Sheet (no hard cap; B12).
- `providers/factory.py` + `providers/registry.py` — the config-driven LLM
  factory (`build_llm`); Gemini default, Groq/OpenAI swappable, model never
  hardcoded; clear error when the key env var is missing.
- `sdk/sdk.py` — the single-entry `SDK` facade with pipeline stubs.
- 51 unit tests (`crewai.LLM` + `os.environ` mocked) at 100% module coverage.

### Phase 3 — Gemini live smoke test
- `crew/smoke.py` — a one-agent / one-task CrewAI crew that replies `pipeline-ok`
  via the provider factory; returns the reply + `token_usage`.
- `SDK.smoke()` records usage through the gatekeeper; `cosmos77-article smoke`
  runs it and prints the reply + Spec-Sheet token line.
- Added `crewai[google-genai]` (the `google-genai` runtime) — CrewAI 1.x's native
  Gemini path requires it; surfaced by the first live call.
- Verified live: `reply: pipeline-ok`, 148 tokens, est. cost $0 (free tier).
  Unit tests keep CrewAI fully mocked (no live calls in the suite).
