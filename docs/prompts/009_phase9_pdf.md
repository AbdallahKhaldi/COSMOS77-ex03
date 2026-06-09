# Prompt log 009 — Phase 9: Compile + PDF QA (THE GATE)

**Phase:** 9 — Compile the PDF and validate it against the §13.1 checklist (B1–B9, B15)
**Authors:** Abdallah Khaldi, Tasneem Natour
**Date:** 2026-06-09

## Prompt issued

> Phase 9 goal: compile the PDF and validate it against the §13.1 technical
> checklist. `scripts/build_pdf.sh` runs `lualatex → biber → lualatex → lualatex`
> in `tex/`. `scripts/qa_pdf.py` asserts: page count ~15, `\includegraphics`,
> a table, a display formula, `\cite` + a non-empty `.bbl`, `\tableofcontents`,
> headers/footers, a Hebrew section, figure PDFs present; scans the `.log` for
> Overfull \hbox; confirms clickable refs. `SDK.build_pdf()` + `SDK.qa_pdf()`;
> CLI `build` + `qa`. Then the manual eyeball.

## What was done (MacTeX-independent infrastructure)

- **`scripts/build_pdf.sh`** — the 4-pass pipeline; **native LuaLaTeX is the
  default**, with an optional `USE_DOCKER_LATEX=1` path (texlive/texlive image) for
  a grader without a local TeX install. Removes a stale `main.pdf` first and fails
  if one is not produced.
- **`latex/qa.py`** — the §13.1 checklist as structured `Check` results (critical
  vs. warning): main.pdf exists, ~15 pages (via pdfplumber), `\includegraphics`,
  figure PDFs, `tabularx`/table, no Overfull \hbox, display formula, TOC,
  headers/footers, a Hebrew section with a babel switch + real Hebrew glyphs,
  `\cite` + a non-empty `.bbl`, and a hyperref `.out`.
- **`scripts/qa_pdf.py`** — thin CLI over `latex.qa` (non-zero exit on a critical fail).
- **`SDK.build_pdf()` / `SDK.qa_pdf()` / `SDK.run()`** (the full end-to-end
  pipeline) + the `cosmos77-article build`, `qa`, and `run` commands.

95 unit tests at 97% coverage (QA validated against passing and failing fixture
projects; CrewAI / lualatex never invoked in the suite — rule 6).

## The compile + eyeball (DONE — native MacTeX 2026)

Compiled with native LuaLaTeX (LuaHBTeX 1.24.0, TeX Live 2026) + biber 2.21 via
the 4-pass pipeline → **`tex/main.pdf`, 25 pages, 218 KB**. Two real issues were
found and fixed during the gate:

1. **"Text line contains an invalid character"** — a stray control byte (`^^H`)
   in an LLM-produced citation title leaked into `refs.bib`. Fixed by stripping
   control characters in `latex/bib.py` (and defensively in `latex/convert.py`).
2. **Overfull \hbox (13)** — added `microtype` + `\emergencystretch` to the
   preamble; down to 2 cosmetic warnings (the table itself never overflows —
   `tabularx`).

A QA false-negative was also fixed: `latex/qa.py` now reads the `\input`-ed
`formula.tex`/`table.tex`/`diagram.tex`, so B7 is detected correctly.

Final state: `scripts/qa_pdf.py` → **ALL CRITICAL CHECKS PASS** (0 fatal errors,
0 undefined citations). **Manual eyeball (every page) confirms B1–B9 + B15:**
cover correct; TOC links jump; running headers/footers; the TikZ diagram + both
matplotlib figures render; the framework table fits; the TCO formula is a
typeset display equation (1); **the Hebrew chapter (ch. 8) reads right-to-left
with English technical terms inline and correct glyphs**; the bibliography lists
13 resolved, clickable references. `tex/main.pdf` is committed (B11).
