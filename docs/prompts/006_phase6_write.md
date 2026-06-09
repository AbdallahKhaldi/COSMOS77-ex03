# Prompt log 006 — Phase 6: Parallel chapter writing

**Phase:** 6 — Generate the chapter bodies (B1, B8, B10)
**Authors:** Abdallah Khaldi, Tasneem Natour
**Date:** 2026-06-09

## Prompt issued

> Phase 6 goal: generate the chapter bodies with writer agents. For each chapter
> in `output/outline.json`, build a `write_task` (~1–1.25 pages of Markdown with
> inline `\cite` markers; `output_file=output/chapters/ch_NN.md`). The Hebrew BiDi
> chapter routes to the `bidi_writer` (Hebrew body, inline English terms). An
> `editor_task` (context = all writes) stitches `output/article.md`.
> `crew.parallel_writers` toggles async; `crew.max_rpm` throttles the free tier.

## What was done

- **`crew/tasks_write.py`** — `write_task` (per chapter; Hebrew instruction when
  `chapter.is_bidi`, English otherwise; `async_execution` driven by config) +
  `editor_task` (context = all writes → `output/article.md`).
- **`crew/write_run.py`** — builds one writer per chapter (BiDi → `bidi_writer`),
  runs the throttled crew, and **deterministically stitches `article.md`** as a
  fallback so the artifact is always complete (Phase 8 typesets the per-chapter
  files, which remain the canonical source).
- **`SDK.write_chapters()`** + the `cosmos77-article write` CLI command.

## The free-tier rate-limit saga (cost awareness — the HW1 weakness, closed)

The first run (12 parallel writers) hit Gemini's free limits hard:
1. **`gemini-2.5-flash` free tier = 5 requests/minute** — parallel writers burst
   straight past it → 429s.
2. Worse, it is **20 requests/day** (`GenerateRequestsPerDayPerProjectPerModel`) —
   far too few for a 12-chapter article. The playbook chose 2.5-flash before
   Google tightened free quotas.

**Fixes, all config-only (no code change — this is exactly what the
provider-agnostic design, B12, is for):**
- Swapped the model to **`gemini/gemini-2.5-flash-lite`** (~1000 RPD / 15 RPM
  free, fresh per-model quota) in `config/providers.json` — one line.
- Set `crew.parallel_writers=false` and `crew.max_rpm=10` in `config/setup.json`:
  on a request-rate-capped free tier, **sequential beats parallel** (parallel
  bursts trigger 429s). The async code path remains and is config-toggleable for a
  paid tier — a real architecture/cost trade-off, recorded in the Spec Sheet.

## Verification (live — free Gemini)

```bash
uv run cosmos77-article write   # 12 chapters → output/chapters/ch_NN.md + article.md
```

12 chapters generated (~600–680 words each), the Hebrew BiDi chapter (ch. 8)
written in Hebrew with inline English technical terms. 75 unit tests, ~99%
coverage; CrewAI fully mocked in the suite (no live calls).
