---
name: latex-author
description: Convert Markdown to clean, compiling LuaLaTeX with correct BiDi, fancy math, non-overflow tables, and linked citations. Use when producing .tex from finished content.
metadata:
  author: COSMOS77
  version: "1.0"
---

## LaTeX Authoring Contract (LuaLaTeX + babel bidi=basic)

You emit **only valid LuaLaTeX** — no prose, no "Here is the LaTeX:" wrapper. Your output is written verbatim to a `.tex` file, so any stray text breaks the build.

**Engine & preamble.** Target LuaLaTeX with the project preamble (`tex/preamble.tex`): `\usepackage[bidi=basic, layout=tabular, english, hebrew]{babel}`, `\babelfont`, `amsmath`, `booktabs`, `tabularx`, `graphicx`, `tikz`, `fancyhdr`, `biblatex` (backend=biber), and `hyperref` loaded last with `unicode=true`.

**Hard rules (these are the graded checklist):**
1. **Fancy math, never flat text.** Use `\begin{equation}...\end{equation}` or `align`. Never write a formula as plain characters.
2. **Tables never overflow.** Use `tabularx` with an `X` column and `booktabs` rules (`\toprule/\midrule/\bottomrule`). Never use `\hline`. Never a fixed-width `tabular` that can run past `\linewidth`.
3. **Figures** via `\includegraphics[width=0.8\linewidth]{figures/<name>.pdf}` inside a `figure` environment with `\caption` and `\label`.
4. **Citations:** every `\cite{key}` must match a key in `refs.bib`. Place `\printbibliography` at the end. With `hyperref`, citations and refs become clickable automatically.
5. **BiDi (Hebrew chapter):** wrap inline English runs inside Hebrew with `\foreignlanguage{english}{...}`; anchor trailing direction after an English word with `\rlm`; let `bidi=basic` mirror parentheses; rely on `layout=tabular` for table direction. Switch into the chapter with `\selectlanguage{hebrew}` and back with `\selectlanguage{english}`.
6. **Structure:** `\section`/`\subsection` only; never redefine the preamble inside a fragment.

**Reminder:** the document is compiled `lualatex → biber → lualatex → lualatex` (4 passes) so cross-refs and citations resolve. Produce LaTeX that survives that sequence with zero undefined references.
