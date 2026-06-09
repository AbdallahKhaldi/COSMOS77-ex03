# Prompt log 005 — Phase 5: Research + outline

**Phase:** 5 — Cited research + a structured 12-chapter outline
**Authors:** Abdallah Khaldi, Tasneem Natour
**Date:** 2026-06-09

## Prompt issued

> Phase 5 goal: the research + planning tasks that produce a cited outline for
> the 15-page article. `research_task` (Researcher, grounded in
> `reference/Agent_Architecture_2026.pdf` + web) → `output/research.md`;
> `outline_task` (Planner, context=research) → a 12-chapter outline (one flagged
> Hebrew BiDi) → `output/outline.md` + machine-readable `output/outline.json`;
> capture citations → `output/citations.json`. `SDK.research()` runs both and
> persists. Tests mock the crew.

## What was done

- **`crew/schemas.py`** — `Outline`/`Chapter`/`Citation` pydantic models so the
  outline task returns *validated* JSON (`Task.output_pydantic`) — no brittle
  parsing of free-form text.
- **`crew/tasks_research.py`** — `research_task` injects an excerpt of the local
  2026 PDF (via `pdfplumber`, config-driven path, graceful fallback) as grounding
  context (more robust than a RAG tool) and writes `output/research.md`;
  `outline_task` returns an `Outline` with exactly one `is_bidi` chapter.
- **`crew/research_run.py`** — runs the sequential crew (`max_rpm` throttle) and
  persists `outline.json`, `citations.json`, and a human `outline.md`.
- **`SDK.research()`** + the `cosmos77-article research` CLI command (CLI refactored
  to a clean dispatch for the growing command set).
- Config: added `paths.reference_pdf` (the source PDF stays *outside* the public
  repo — not redistributed — and is grounded by path when present).

## Verification (live — free Gemini)

```bash
uv run cosmos77-article research
# research: 12 chapters, 9 citations
# token_usage: {... total_tokens: 43974, successful_requests: 4, estimated_cost_usd: 0.0}
```

Produced a 12-chapter outline (exactly **1 Hebrew BiDi** chapter), 9 BibTeX-ready
citations, and a 14.8 KB grounded `research.md`. 70 unit tests, 99% coverage; the
suite keeps CrewAI fully mocked (no live calls in tests).
