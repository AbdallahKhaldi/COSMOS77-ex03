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

## The compile + eyeball (gated on the local MacTeX install)

`lualatex`/`biber` come from the user's MacTeX install. The compile + the §13.1
QA + the manual page-by-page eyeball (cover, TOC links, BiDi RTL, table fit,
fancy formulas, the Python figure, clickable citations) complete this phase and
produce the committed `tex/main.pdf`. (Recorded here once the compile is green.)
