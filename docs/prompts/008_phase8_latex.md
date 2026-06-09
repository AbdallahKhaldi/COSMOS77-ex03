# Prompt log 008 — Phase 8: LaTeX assembly (Markdown → tex/)

**Phase:** 8 — Turn the chapters + figures + citations into a LuaLaTeX project (B11)
**Authors:** Abdallah Khaldi, Tasneem Natour
**Date:** 2026-06-09

## Prompt issued

> Phase 8 goal: assemble a complete LuaLaTeX project in `tex/`. `tex/preamble.tex`
> (the §16 LuaLaTeX + babel(bidi=basic) + biblatex/biber + hyperref preamble);
> `tex/main.tex` (cover, `\tableofcontents`, `\input` each section, the table,
> formula, figures, TikZ diagram, Hebrew chapter, `\printbibliography`);
> `latex/assemble.py` (deterministic builder: chapters → `tex/sections/`, write
> `tex/refs.bib` from `citations.json`); `crew/tasks_latex.py` (latex_author task).
> `SDK.assemble_latex()`. Emit ONLY LaTeX (no wrapper).

## Architecture decision — deterministic assembly (ADR-004)

The PDF is the heart of the grade, so it **must** compile cleanly. Rather than
risk LLM wrapper-text / escaping / BiDi bugs in the graded `.tex`, Phase 8 uses a
**deterministic Markdown→LaTeX assembler**:

- `latex/convert.py` — `md_to_latex()`: headings → `\section`/`\subsection`,
  paragraphs, lists, `**bold**`/`*italic*`/`` `code` ``, careful LaTeX escaping that
  **preserves inline `\cite{...}`**, strips stray code fences, and wraps the Hebrew
  chapter in `\selectlanguage{hebrew}` for BiDi (B8).
- `latex/bib.py` — `build_refs_bib()`: a `@misc` entry per citation **plus a
  placeholder for any cited key without a record**, so the bibliography never has
  an undefined reference (B9 "citations resolve").
- `latex/document.py` — `build_main_tex()`: cover page from config (B2), TOC (B3),
  section inputs with the diagram (B4) + adoption figure (B5) + table (B6) +
  frameworks figure + TCO formula (B7) interleaved, then `\printbibliography` (B9).
- `latex/assemble.py` — orchestrates all of it.

The latex-author Skill + agent (Phase 4) and `crew/tasks_latex.py` encode the LLM
conversion contract (B10/B13) and remain available; the deterministic path is the
default for build reliability.

## Verification

```bash
uv run cosmos77-article assemble
# assemble: 12 sections; refs.bib + main.tex written
ls tex/sections/*.tex   # 12 ; tex/main.tex + tex/refs.bib present
grep -c 'selectlanguage{hebrew}' tex/sections/ch_08.tex   # 1 (BiDi chapter)
grep -c '@misc{' tex/refs.bib                              # 13 (all cited keys resolve)
```

A Python 3.11 gotcha bit once: f-string expression parts can't contain
backslashes — the list-item regex was refactored out of the f-string. 92 unit
tests, 97.8% coverage. The actual `lualatex→biber→lualatex→lualatex` compile is
Phase 9 (pending the local MacTeX install).
