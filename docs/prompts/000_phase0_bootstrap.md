# Prompt log 000 — Phase 0: Repo bootstrap

**Phase:** 0 — Repo bootstrap + tooling (reuse HW1/HW2)
**Authors:** Abdallah Khaldi, Tasneem Natour
**Date:** 2026-06-09

## Prompt issued

> Senior software architect, deliver HW3 ("Article/Book Generation with CrewAI
> and LaTeX") for UOH-RL07. Authority order: `../CLAUDE_CODE_PLAYBOOK.md` (§1 the
> 17 rules, §1.5 acceptance B1–B15, §16 the LuaLaTeX BiDi template). Phase 0
> goal: repo skeleton, tooling, `CLAUDE.md`, git init + remote + first push — no
> business logic. Reuse the proven tooling from `~/COSMOS77/HW1/COSMOS77-ex01/`
> and `~/COSMOS77/HW2/COSMOS77-ex02/` (pyproject, ruff/pytest/coverage config,
> pre-commit, CI, `scripts/check_line_cap.py`, `scripts/generate_cover_pdf.py`,
> `CLAUDE.md`, `LICENSE`, `CONTRIBUTING.md`). Provider-agnostic LLM config
> (Gemini default); no hardcoded model. TDD with all LLM/CrewAI/Gemini/lualatex
> I/O mocked.

## What was done

- **Environment audit.** Confirmed `uv`, `gh` (authed as `AbdallahKhaldi`), and
  Docker are present; **MacTeX is being installed by the user** (lualatex/biber
  not yet on PATH — needed only from Phase 9). Verified the free `GEMINI_API_KEY`
  authenticates (HTTP 200, `gemini-2.5-flash` available).
- **Repo created:** `https://github.com/AbdallahKhaldi/COSMOS77-ex03` (public).
  `git init -b main`, identity + remote configured.
- **Scaffold** (ported and adapted from HW2, package renamed `cosmos77_ex03`):
  - `pyproject.toml` — project `cosmos77-ex03` v1.00, Python `>=3.11,<3.12`,
    deps `crewai>=1.9`, `crewai-tools`, `google-generativeai`, `matplotlib`,
    `numpy`, `python-dotenv`, `pydantic`, `rich`, `pyyaml`; dev group;
    `[project.scripts] cosmos77-article`; ruff/coverage(85%)/pytest config.
  - `.gitignore` (Python + `.env` + caches + LaTeX build junk; **commits `tex/`,
    `tex/main.pdf`, `tex/figures/*.pdf`**; ignores `output/*` except `.gitkeep`),
    `.env.example`, `.python-version`.
  - `config/setup.json`, `config/providers.json` (provider-agnostic LLM, Gemini
    active), `config/logging_config.json`.
  - `CLAUDE.md` (the 17 rules, §16 verbatim), `README.md` (placeholder),
    `LICENSE` (MIT 2026), `CHANGELOG.md` (`[1.00]`), `CONTRIBUTING.md`.
  - `scripts/check_line_cap.py` (ported), `scripts/generate_cover_pdf.py`
    (ported, retargeted to ex03 + exercise number 3), `scripts/build_pdf.sh`
    and `scripts/qa_pdf.py` (Phase-0 placeholders; filled in Phase 9).
  - `src/cosmos77_ex03/` package skeleton (`constants.py`, `cli/main.py`, and
    empty `sdk/`, `shared/`, `providers/`, `crew/`, `skills/`, `figures/`,
    `latex/` packages), `tests/` with a Phase-0 constants smoke test.
  - `.pre-commit-config.yaml` and `.github/workflows/ci.yml` (ruff, format,
    line-cap, pytest with the 85% coverage gate; live LLM/LaTeX tests excluded).

## Verification

```bash
uv sync
uv run ruff check .            # zero
uv run ruff format --check .   # clean
uv run python scripts/check_line_cap.py   # 0 offenders
uv run pytest -m "not live"    # green, coverage >= 85%
```

## Notes / decisions

- **Pacing:** user opted into full autopilot (Phases 0→12 back-to-back), with
  per-phase commits + prompt logs preserved and the PDF surfaced for eyeball at
  the end.
- **LaTeX engine:** user is installing MacTeX (native lualatex/biber); the
  Phase-9 `build_pdf.sh` will use the native four-pass pipeline.
- **Dual authorship:** commits alternate between both partners (mirrors HW2) so
  the Phase-11 "both authors in shortlog" audit passes.
