# PRD — LuaLaTeX BiDi Template & Compile Pipeline (B2/B3/B11)

## 1. Purpose & scope

This PRD specifies the LaTeX project that the CrewAI `latex-author` agent
populates and that `scripts/build_pdf.sh` compiles into `tex/main.pdf` — the
heart of the HW3 grade. It owns three deliverables end to end:

- `tex/preamble.tex` — the LuaLaTeX + BiDi + biblatex preamble (the canonical
  document class, fonts, packages, header/footer policy).
- `tex/main.tex` — the document skeleton: cover page (B2), `\tableofcontents`
  and running headers/footers (B3), `\input` of section files, and
  `\printbibliography`.
- `scripts/build_pdf.sh` — the deterministic four-pass compile
  `lualatex -> biber -> lualatex -> lualatex` (B11).

The proven starting point is the prebuilt smoke-test at
`~/COSMOS77/HW3/prebuilt/tex_sample/` (`main.tex`, `build.sh`, `refs.bib`,
`make_figure.py`). That sample already renders every §13.1 element and the
Hebrew BiDi chapter; this PRD lifts its preamble verbatim into `tex/preamble.tex`
and splits the monolithic sample into preamble + skeleton + sections.

Out of scope here (owned by sibling PRDs): chapter prose generation, the
matplotlib figure pipeline, the provider-agnostic LLM config, and the Spec Sheet.
This document only guarantees the template compiles and exposes the structural
hooks those agents fill.

## 2. Acceptance-criteria mapping

| Criterion | What this template provides |
|-----------|------------------------------|
| B1 (~15 pages) | `\input` skeleton + `12pt,a4paper` class sized for ~15 pages |
| B2 (cover) | `titlepage` with title/author/date/course/instructor from `config/setup.json` |
| B3 (TOC + headers) | `\tableofcontents` + `fancyhdr` `\leftmark`/`\thepage` running heads/feet |
| B4 (TikZ image) | `tikz` + libraries loaded; diagram float in a section file |
| B5 (Python graph) | `graphicx` `\includegraphics{figures/adoption.pdf}` slot |
| B6 (table) | `tabularx`+`booktabs` non-overflow table pattern |
| B7 (fancy formula) | `amsmath` display `equation` with `\label`/`\eqref` |
| B8 (Hebrew BiDi) | `babel(bidi=basic, layout=tabular)` + `\babelfont`/`\foreignlanguage` |
| B9 (bibliography) | `biblatex` backend=biber + `\addbibresource` + clickable cites |
| B11 (tex/ builds) | `tex/` committed; `build_pdf.sh` four-pass compile |
| B15 (wrapper QA) | links resolve, cites exist, BiDi correct, tables fit, formulas typeset |

## 3. File layout & responsibilities

```
tex/
  preamble.tex      # documentclass + all \usepackage; loaded by main.tex
  main.tex          # \input{preamble}; titlepage; toc; \input sections; biblio
  sections/         # ch_NN.tex written by chapter-writer agents
  figures/          # adoption.pdf and any TikZ-external output
  refs.bib          # biblatex database (\addbibresource target)
scripts/
  build_pdf.sh      # four-pass compile, --interaction=nonstopmode
```

`tex/preamble.tex` is `\input` (not `\usepackage`) from `main.tex` so the
document class line stays first and hyperref stays last across the boundary.
The `latex-author` agent writes `main.tex` and the section files; it never
edits `preamble.tex` except through the templated values in §4.

## 4. Cover-page data binding (B2)

The cover values are configuration, never hardcoded (Rule 4). They are sourced
from `config/setup.json -> article`:

| LaTeX field | config key | example value |
|-------------|-----------|---------------|
| title | `article.title` | "AI Agents in Production: …" |
| author | `article.author` | "Abdallah Khaldi and Tasneem Natour" |
| course | `article.course` | "Orchestration of AI Agents (203.3763)" |
| instructor | `article.instructor` | "Dr. Yoram Segal" |
| date | `\today` | rendered at compile time |

The SDK (`src/cosmos77_ex03/sdk/sdk.py`) reads `setup.json` and the
`latex` module (`src/cosmos77_ex03/latex/`) renders the `titlepage` block by
string substitution into `main.tex`; the ampersand in the course name is
escaped to `\&`. No author/title literal appears in any `.py` file.

## 5. Canonical preamble (`tex/preamble.tex`)

Reproduced verbatim from the playbook Appendix B / prebuilt sample. Package
order is load-bearing: `documentclass` first, `hyperref` last.

```latex
% !TEX program = lualatex
\documentclass[12pt,a4paper]{article}

% ---- BiDi + languages (English primary, Hebrew for the BiDi chapter) -------
\usepackage[bidi=basic, layout=tabular, english, hebrew]{babel}
\babelprovide[main, import]{english}
\babelprovide[import]{hebrew}

% ---- Fonts (FreeSerif covers Latin+Hebrew; macOS fallbacks below) ----------
\babelfont{rm}{FreeSerif}
% \babelfont[hebrew]{rm}{Arial Hebrew}   % macOS system-font fallback
% \babelfont[hebrew]{rm}{David CLM}      % Culmus fallback

% ---- Packages --------------------------------------------------------------
\usepackage{amsmath, amssymb}              % fancy math (B7)
\usepackage{booktabs, tabularx}            % non-overflow tables (B6)
\usepackage{graphicx}                      % Python-generated figure (B5)
\usepackage{tikz}\usetikzlibrary{shapes.geometric, arrows.meta, positioning}
\usepackage{fancyhdr}                      % headers/footers (B3)
\usepackage[backend=biber, style=numeric, sorting=none]{biblatex}
\addbibresource{refs.bib}
\usepackage[colorlinks=true, linkcolor=blue, citecolor=blue, urlcolor=blue,
            unicode=true]{hyperref}        % MUST load LAST

\pagestyle{fancy}\fancyhf{}
\fancyhead[L]{\nouppercase{\leftmark}}
\fancyhead[R]{\thepage}
\fancyfoot[C]{COSMOS77 — 203.3763 HW3}
\hypersetup{pdftitle={AI Agents in Production}, pdfauthor={COSMOS77}}
```

### Why each line exists

- `documentclass[12pt,a4paper]{article}` — `article` (not `book`); HW3 is an
  article, sized to ~15 pages (B1).
- `babel[bidi=basic, layout=tabular, english, hebrew]` — `bidi=basic` is the
  LuaLaTeX-native bidirectional engine; `layout=tabular` keeps tables/columns
  in logical order under BiDi (prevents B6 tables from mirroring). English is
  declared first and confirmed main via `\babelprovide[main, import]{english}`
  so the document direction is LTR with a Hebrew island (B8).
- `\babelfont{rm}{FreeSerif}` — one Unicode font for both scripts; FreeSerif
  ships with TeX Live / MacTeX. On macOS, uncomment the `Arial Hebrew` line if
  Hebrew glyphs render as tofu boxes; Culmus `David CLM` is the third option.
- `amsmath` is required for the display `equation` to typeset as a real formula,
  not flat text (B7/B15).
- `biblatex` with `backend=biber` + `\addbibresource{refs.bib}` is the only
  bibliography mechanism; `style=numeric, sorting=none` gives `[1]`-style
  clickable citations in document order (B9).
- `hyperref` loads last with `unicode=true` so PDF bookmarks and the Hebrew
  citation/section anchors are UTF-8 clean and every `\cite`/`\ref` is a live
  link (B9/B15). Loading it before biblatex/babel would break link targets.

## 6. Document skeleton (`tex/main.tex`)

`main.tex` is intentionally thin — structure only, prose lives in `sections/`:

1. `\input{preamble}` — pulls in §5.
2. `\begin{document}`.
3. `titlepage` cover block (B2) with the §4 substituted values, centered,
   `\today` for the date.
4. `\tableofcontents\newpage` (B3) — populated on pass 2+ from the `.toc` aux.
5. `\input{sections/ch_01}` … `\input{sections/ch_12}` (`num_chapters: 12`
   from `setup.json`). Each `ch_NN.tex` is one `\section`; the chapter-writer
   agents own their content, including the Hebrew chapter (B8), the TikZ
   diagram (B4), the matplotlib `\includegraphics` (B5), the `tabularx` table
   (B6), and at least one `amsmath` formula (B7).
6. `\printbibliography[title={References / ביבליוגרפיה}]` (B9).
7. `\end{document}`.

The running header pulls the current `\section` title via `\leftmark` (left)
and page number via `\thepage` (right); the footer is a fixed course string —
satisfying the "running headers/footers" half of B3.

## 7. Compile pipeline (`scripts/build_pdf.sh`) — B11

The four-pass sequence is mandatory and ordered: TOC and cross-references need
two LaTeX passes to stabilize the `.aux`/`.toc`; biber must run between them to
resolve `\addbibresource` into `.bbl`; the final pass binds hyperref anchors so
every citation and `\ref` clicks through.

```bash
set -e
cd "$(dirname "$0")/../tex"
lualatex --interaction=nonstopmode main.tex   # pass 1: emit .aux/.toc, cite keys
biber    main                                 # resolve refs.bib -> main.bbl
lualatex --interaction=nonstopmode main.tex   # pass 2: inject bibliography + TOC
lualatex --interaction=nonstopmode main.tex   # pass 3: settle page refs + links
```

- `lualatex` (not `pdflatex`/`xelatex`) — required for `bidi=basic` and
  `\babelfont` (OpenType fonts via fontspec).
- `--interaction=nonstopmode` keeps the build non-interactive and deterministic
  (Rule 17); a real error still aborts via `set -e`.
- The figure is generated upstream by the figure agent into
  `tex/figures/adoption.pdf` before this script runs; the script does not call
  matplotlib (separation of concerns from the prebuilt sample's `make_figure.py`).
- In the test suite this entire subprocess is mocked (Rule 6) — no live
  `lualatex`/`biber` runs in CI; tests assert the command sequence and argument
  order, not a produced PDF.

## 8. QA gate (`scripts/qa_pdf.py`) — B15

After a real build, `qa_pdf.py` asserts the technical-wrapper correctness that
B15 grades, and feeds a pass/fail into the Spec Sheet:

- page count is in the ~15 range (`pdfinfo`-style page probe) — B1.
- the bibliography section exists and `\cite` keys all resolve (no `[?]`) — B9.
- the Hebrew chapter is present and direction switches back to English cleanly
  after `\selectlanguage{english}` — B8.
- the `tabularx` table does not overfull the line (no overflow box warnings) — B6.
- the formula is a typeset `equation` (display math), not literal text — B7.

## 9. Constraints, risks & decisions

- **No live LaTeX in tests** — all `subprocess` calls to `lualatex`/`biber` are
  mocked; the build script is validated by asserting the four-pass order
  (Rule 6, Rule 17).
- **Hebrew font portability** — FreeSerif is the default; the macOS grading box
  is covered by the commented `Arial Hebrew` fallback. The QA gate flags tofu so
  a missing-font regression cannot silently ship (B8/B15).
- **hyperref-last invariant** — enforced by keeping the preamble in one
  `\input` file the `latex-author` agent does not reorder; any reordering breaks
  B9 links and is caught by `qa_pdf.py`.
- **layout=tabular over layout=sectioning** — chosen so BiDi does not mirror
  the `tabularx` columns; protects B6 while still flipping Hebrew text (B8).
- **One Hebrew chapter only, Arabic forbidden** — the BiDi island is scoped to a
  single `\section` via `\selectlanguage`; no Arabic appears anywhere (canon).
- **Sample-first** — `tex/` is seeded from the proven
  `~/COSMOS77/HW3/prebuilt/tex_sample/` so the toolchain is validated before the
  crew runs; the crew only adds prose into `sections/` and entries into
  `refs.bib`.
