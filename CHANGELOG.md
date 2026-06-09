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

### Phase 4 — CrewAI agents + Skills
- 3 CrewAI Skills under `skills/{researcher,technical-writer,latex-author}/SKILL.md`
  (verified a real `Agent` loads each from disk; B13).
- `crew/agents.py` — 7 agent factories (researcher, planner, per-chapter
  chapter_writer, figure_agent, bidi_writer, editor, latex_author) with skills
  wired by absolute path and `allow_delegation=False` (ADR-002; B10).
- `crew/tools.py` — web-search tool selection (Serper or keyless scraper) +
  FileWriterTool; `SDK.build_agents()` returns the roster.
- 64 unit tests at 100% coverage (`crewai.Agent` + `crewai_tools` mocked).

### Phase 5 — Research + outline
- `crew/schemas.py` — `Outline`/`Chapter`/`Citation` models; the outline task uses
  `Task.output_pydantic` for validated, machine-readable JSON.
- `crew/tasks_research.py` — PDF-grounded research task (pdfplumber, config-driven
  path) + a structured outline task (exactly one Hebrew BiDi chapter).
- `crew/research_run.py` + `SDK.research()` + `cosmos77-article research` — persist
  `output/{research.md,outline.json,citations.json,outline.md}`.
- Verified live: 12 chapters, 1 BiDi, 9 citations, ~44k tokens, $0. 70 tests, 99% cov.

### Phase 6 — Parallel chapter writing
- `crew/tasks_write.py` + `crew/write_run.py` + `SDK.write_chapters()` +
  `cosmos77-article write` — one writer per chapter (Hebrew BiDi chapter → the
  `bidi_writer`); editor stitches `output/article.md` (deterministic fallback).
- **Free-tier fix (config-only, B12):** `gemini-2.5-flash` free tier is 5 RPM /
  20 RPD — too small. Swapped to `gemini-2.5-flash-lite` in `providers.json`; set
  `parallel_writers=false` + `max_rpm=10` in `setup.json` (sequential beats
  parallel bursts on a rate-capped tier). The async path stays, config-toggleable.
- Verified live: 12 chapters written (Hebrew chapter 8 in Hebrew). 75 tests, 99% cov.

### Phase 7 — Figures, table, formula, Python graph
- `figures/charts.py` — deterministic matplotlib `adoption.pdf` (the B5 graph) and
  `frameworks.pdf`; `SDK.make_figures()` + `cosmos77-article figures`.
- `tex/diagram.tex` (TikZ architecture, B4), `tex/table.tex` (tabularx/booktabs,
  B6), `tex/formula.tex` (fancy amsmath TCO equation, B7).
- 80 tests at 99% coverage (PDF validity + LaTeX-snippet content checks).

### Phase 8 — LaTeX assembly (Markdown → tex/)
- `tex/preamble.tex` — LuaLaTeX + babel(bidi=basic) + biblatex/biber + hyperref.
- `latex/convert.py` (Markdown→LaTeX, `\cite`-preserving, Hebrew BiDi wrapping),
  `latex/bib.py` (refs.bib with every cited key resolved), `latex/document.py`
  (cover + TOC + interleaved visuals + bibliography), `latex/assemble.py`.
- `crew/tasks_latex.py` (latex_author task, B13) + `SDK.assemble_latex()` +
  `cosmos77-article assemble`. Deterministic assembly for a guaranteed clean
  compile (ADR-004); the LLM latex-author path remains available.
- Verified: 12 sections + main.tex + refs.bib (13 entries); ch_08 BiDi-wrapped.
  92 tests, 97.8% coverage.
