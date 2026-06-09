# Acceptance audit — B1–B15 + the 17 rules

Final verification for COSMOS77-ex03 (HW3). Every acceptance criterion mapped to
where it is satisfied, the evidence, and its status. Generated at Phase 11.

## Acceptance criteria (spec §13 / playbook §1.5)

| # | Requirement | Where satisfied | Evidence | Status |
|---|---|---|---|---|
| **B1** | ~15-page PDF | `tex/main.pdf` | 25 pages (`qa_pdf` B1; eyeballed) | ✅ (exceeds) |
| **B2** | Cover sheet | `latex/document.py` titlepage → `tex/main.tex` | PDF p.1: title, both authors, course, Dr. Segal, date | ✅ |
| **B3** | TOC + chapters + headers/footers | `\tableofcontents`; `fancyhdr` in `tex/preamble.tex` | PDF p.2 + running head/foot on every page | ✅ |
| **B4** | ≥1 image | `tex/diagram.tex` (TikZ) | PDF p.4, Fig. 1 (four-layer architecture) | ✅ |
| **B5** | ≥1 Python-generated graph | `figures/charts.py` → `tex/figures/*.pdf` | PDF p.4 Fig. 2 + p.13 Fig. 3 | ✅ |
| **B6** | ≥1 non-overflow table | `tex/table.tex` (`tabularx`+`booktabs`) | PDF p.13, Table 1, fits `\linewidth` | ✅ |
| **B7** | ≥1 fancy formula | `tex/formula.tex` (`amsmath`) | PDF p.24, Eq. (1) TCO (sum, sub/superscripts, `\underbrace`) | ✅ |
| **B8** | Hebrew–English BiDi chapter | `crew/agents.py` bidi_writer + `latex/convert.py` (`\selectlanguage{hebrew}`) | PDF p.12–15, Ch. 8, RTL + inline English | ✅ |
| **B9** | Linked bibliography | `biblatex`+`biber`+`hyperref`; `tex/refs.bib` | PDF p.24–25, 13 clickable resolved refs | ✅ |
| **B10** | Real CrewAI multi-agent team | `crew/agents.py` (7 roles), `crew/research_run.py`, `crew/write_run.py` | Live runs: research (4 reqs) + write (169 reqs) | ✅ |
| **B11** | `tex/` project + builds | `tex/` committed; `scripts/build_pdf.sh` | `lualatex→biber→lualatex→lualatex`, 0 fatal errors | ✅ |
| **B12** | Provider-agnostic + Spec Sheet | `providers/factory.py`; `output/spec_sheet.json` | One-line model swap; 1.3M tokens, $0 | ✅ |
| **B13** | CrewAI Skills | `skills/{researcher,technical-writer,latex-author}/SKILL.md` | wired by path; verified a real `Agent` loads each | ✅ |
| **B14** | PRD/PLAN/TODO + README | `docs/PRD*.md`, `docs/PLAN.md`, `docs/TODO.md`, `README.md` | 11 PRDs, C4+ADRs, 651 TODOs, 256-line README | ✅ |
| **B15** | Technical-wrapper correctness | `scripts/qa_pdf.py` + manual eyeball | all critical checks pass; links/citations/BiDi/table/formula verified | ✅ |

## The 17 rules

| Rule | Status |
|---|---|
| 1. ≤150 lines/.py | ✅ `check_line_cap.py` passes (no offenders) |
| 2. Single SDK entry | ✅ `sdk/sdk.py` is the only business-logic surface |
| 3. OOP, no duplication | ✅ shared modules; converter/bib/document split |
| 4. Zero hardcoded config | ✅ `config/*.json` + `.env`; model never hardcoded |
| 5. uv only | ✅ no pip/venv; `uv.lock` committed |
| 6. TDD, all I/O mocked | ✅ 96 tests; no live LLM/CrewAI/lualatex in the suite |
| 7. Coverage ≥85% | ✅ 97.55% |
| 8. ruff zero | ✅ `ruff check` clean; `ruff format --check` clean |
| 9. No secrets in repo | ✅ `.env` gitignored; scrub-test fixture sanitized (Phase 11) |
| 10. Versioning 1.00 | ✅ `version.py` + every config + (tag at Phase 12) |
| 11. Conventional commits | ✅ 60 commits, 0 wip/tmp/fixup |
| 12. Prompt log | ✅ `docs/prompts/000`–`011` |
| 13. Gatekeeper cost meter | ✅ `shared/gatekeeper.py` → Spec Sheet |
| 14. CLI only; generated article | ✅ produced by the crew, not hand-written |
| 15. Docstrings | ✅ public modules/classes/functions |
| 16. Type hints | ✅ public signatures; no bare `Any` surface |
| 17. Deterministic tests | ✅ seeded; mocked; no flakes |

## Reproducibility & gauntlet

- `ruff check` ✅ · `ruff format --check` ✅ · `check_line_cap.py` ✅ · `pytest --cov-fail-under=85` ✅ (96 passed, 97.55%).
- `uv lock --check` ✅ · `.env` not tracked ✅ · no real key material in tracked files ✅ (Phase-11 fixture fix).
- Both authors in `git shortlog` ✅ (Abdallah 33 / Tasneem 27) · 60 commits ≥ 30 ✅.
- **Deterministic build chain reproduces:** `assemble → build → qa` regenerates a
  25-page `tex/main.pdf` with all critical checks passing.
- The stochastic LLM phases (research/write) were verified live in Phases 5–6 and
  are re-runnable via `cosmos77-article run`; they are intentionally **not** re-run
  here to preserve the eyeballed, committed PDF and the free-tier quota.

## Note carried to the user (security)

Git history contains a 34-char **prefix** (not the full key) of the free,
disposable Gemini key, from an early test fixture (fixed in Phase 11). The key is
free and regenerable; recommended action is to rotate it at aistudio.google.com
if desired. No full key is in any tracked file or in history.
