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
