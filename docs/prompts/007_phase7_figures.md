# Prompt log 007 — Phase 7: Figures, table, formula, Python graph

**Phase:** 7 — The mandatory visual/quantitative elements (B4, B5, B6, B7)
**Authors:** Abdallah Khaldi, Tasneem Natour
**Date:** 2026-06-09

## Prompt issued

> Phase 7 goal: the mandatory visual/quantitative elements — deterministic Python,
> minimal/no LLM. `figures/charts.py` (matplotlib → `tex/figures/*.pdf`):
> `adoption_curve()` (the enterprise agent-adoption projection, B5) and
> `framework_fit()`. A TikZ block diagram (B4 image), a `tabularx`+`booktabs`
> table that fits (B6), and a fancy `amsmath` display formula (B7).
> `SDK.make_figures()` runs the charts and verifies the PDFs.

## What was done

- **`figures/charts.py`** — deterministic (fixed data, `Agg` backend) matplotlib
  figures: `adoption.pdf` (enterprise AI-agent adoption 2023→2026, the B5 graph)
  and `frameworks.pdf` (framework production-fit). `generate_all()` writes both.
- **`tex/diagram.tex`** — a TikZ four-layer production-agent architecture diagram
  (Planning / Memory / Tools / Observability) with a feedback loop — the B4 image.
- **`tex/table.tex`** — a `tabularx` (`X` column) + `booktabs` framework-comparison
  table that never overflows `\linewidth` (no `\hline`); B6.
- **`tex/formula.tex`** — a fancy `amsmath` display equation: the agent TCO model
  with `\underbrace`, a sum, and sub/superscripts (not flat text); B7.
- **`SDK.make_figures()`** + the `cosmos77-article figures` CLI command.

## Verification

```bash
uv run cosmos77-article figures
ls tex/figures/*.pdf   # adoption.pdf (13.7 KB), frameworks.pdf (16.1 KB)
```

80 unit tests at 99% coverage: `charts.generate_all` writes valid (`%PDF`) PDFs;
content checks confirm the table uses `tabularx`/`booktabs` (no `\hline`), the
formula is a display `equation`, and the diagram is a captioned `tikzpicture`.
