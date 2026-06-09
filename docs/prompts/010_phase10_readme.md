# Prompt log 010 — Phase 10: README lab report + Spec Sheet

**Phase:** 10 — The README the grader reads first + the Spec Sheet (B12, B14)
**Authors:** Abdallah Khaldi, Tasneem Natour
**Date:** 2026-06-09

## Prompt issued

> Phase 10 goal: the README lab report (≥250 lines, ≥3 images), embedding 2–3
> screenshots of `tex/main.pdf`, the architecture diagrams, quickstart, the
> config-swap, the §13.1 → page-number map, the Spec Sheet (interpreted, not just
> dumped), how-we-used-AI-agents, how-to-extend, testing, and the self-assessment
> (85). `SDK.spec_sheet()` writes `output/spec_sheet.json`. Confirm `tex/` +
> `tex/main.pdf` committed.

## What was done

- **`README.md`** (256 lines, 17 sections, 3 embedded PDF screenshots + CI/coverage
  badges): abstract, what-it-produces, architecture (C4 pointer + a Mermaid run
  sequence), repository layout, quickstart, the 8 CLI commands, the one-line
  provider swap (B12), the crew + 3 Skills, the **B1–B9 → page-number table**, the
  Spec Sheet table + interpretation, the prompt-log pointer, extension points,
  limitations, testing/quality, license, and the self-assessment (85).
- **Screenshots** rendered from `tex/main.pdf` via PyMuPDF → `assets/cover.png`,
  `assets/diagram_figure.png`, `assets/hebrew_chapter.png`.
- **`output/spec_sheet.json`** — the real measured aggregate across the runs
  (1,302,558 tokens, 174 requests, **$0** on the free tier); un-ignored in
  `.gitignore` so it ships as a B12 deliverable. `SDK.write_spec_sheet()` persists
  it programmatically (tested).

## Spec-Sheet interpretation (closes the HW1 "numbers aren't analysis" gap)

The **write** phase is ~97% of tokens (12 chapter-writers + an Editor that ingests
the full article + CrewAI reasoning loops). Research is ~3%. Cost is $0 (free
Gemini). The first scaling lever for a longer book is chunking the editor's
single-pass stitch; a paid tier would re-enable parallel writers (disabled here
by the free-tier RPM cap).

## Verification

```bash
wc -l README.md            # 256  (>= 250)
grep -c '!\[' README.md    # 5    (>= 3 images)
test -f output/spec_sheet.json && test -f tex/main.pdf && echo OK
uv run ruff check . && uv run pytest -m "not live"   # clean, 96 passed, 97.5% cov
```
