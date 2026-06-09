# PRD — Figures, Graph, Table, Formula (B4/B5/B6/B7)

## 1. Purpose & Scope

This PRD specifies the deterministic visual and structural assets of the
COSMOS77-ex03 article *"AI Agents in Production: Architecture, Orchestration &
Governance in 2026"*. It covers four acceptance criteria that are produced with
**minimal or zero LLM involvement** so they are reproducible byte-for-byte
across builds:

| Item | Acceptance | Producer | Output artifact |
|------|-----------|----------|-----------------|
| Python-generated graph | **B5** | `figures/charts.py::adoption_curve()` | `tex/figures/adoption.pdf` |
| Python-generated graph (support) | **B5** | `figures/charts.py::framework_fit()` | `tex/figures/frameworks.pdf` |
| TikZ block diagram (image) | **B4** | `tex/figures/diagram_tikz.tex` | inlined TikZ picture |
| Comparison table | **B6** | `tex/latex/table.tex` | `\input`-ed snippet |
| Fancy display formula | **B7** | `tex/latex/formula.tex` | `\input`-ed snippet |

These assets feed `tex/main.tex` and are part of the committed `tex/` project
(**B11**), are exercised by deterministic tests (**B15**), and contribute to the
~15-page target (**B1**).

## 2. Design Principles

- **Determinism over creativity.** Charts are seeded; no randomness leaks into a
  build. Re-running `scripts/build_pdf.sh` regenerates identical PDFs.
- **No LLM in the figure path.** The matplotlib code is pure Python with
  hardcoded *domain data* (not config). Hardcoded *data values* are allowed; what
  is forbidden by the 17 RULES is hardcoded *configuration* (provider, model,
  paths) — those still resolve from `config/*.json`.
- **150-line hard cap per `.py`.** `charts.py` stays under the cap; if it grows,
  split shared plot styling into `figures/style.py` and a data module
  `figures/datasets.py`.
- **Separation of concerns.** Python emits PDFs only; LaTeX owns layout. The
  diagram, table, and formula are authored directly in LaTeX (no Python).
- **OOP / no duplication.** Common figure scaffolding (figure size, font, grid,
  `savefig` call) is factored into one helper consumed by both chart functions.

## 3. Python Graphs — `src/cosmos77_ex03/figures/charts.py` (B5)

### 3.1 Module contract

- Public functions are typed and docstringed (17 RULES: docstrings + type hints
  on public surfaces).
- Backend is forced to non-interactive PDF before importing `pyplot`:
  ```python
  import matplotlib
  matplotlib.use("pdf")
  import matplotlib.pyplot as plt
  ```
- Output directory is resolved from `config/setup.json` (key
  `paths.tex_figures_dir`, default `tex/figures`), never hardcoded.
- A private helper centralizes styling and saving:
  ```python
  def _save(fig: "Figure", name: str) -> Path:
      out = figures_dir() / name
      fig.savefig(out, format="pdf", bbox_inches="tight")
      plt.close(fig)
      return out
  ```

### 3.2 `adoption_curve() -> Path`

- Renders the **Gartner ~5% → 40% enterprise agentic-AI adoption projection,
  2025 → 2026** as a labeled line/area chart.
- Data is a fixed, ordered series (quarterly points from 2025 through 2026)
  defined as a module constant `ADOPTION_SERIES`.
- Determinism: no RNG used; if any jitter/annotation offset is computed it is
  derived from a fixed `numpy.random.default_rng(seed=...)` seeded from
  `setup.json` (`figures.seed`, default `77`).
- Labels: title, axis labels (`Year/Quarter`, `Enterprise adoption (%)`),
  annotated start (~5%) and end (~40%) markers, percentage y-formatter.
- Saves to `adoption.pdf`. This is the **B5** primary figure.

### 3.3 `framework_fit() -> Path`

- Compares **LangGraph, CrewAI, AutoGen, LlamaIndex, PydanticAI, DSPy** on a
  single "production fit" axis (horizontal bar or radar; bar chosen for
  page-fit and BiDi-neutral rendering).
- Data is constant `FRAMEWORK_FIT` (framework → score), ordered descending for
  readable ranking.
- Deterministic colors via an explicit palette list (no colormap sampling that
  could shift between matplotlib versions).
- Saves to `frameworks.pdf`. Supports B5 and is referenced from the
  orchestration/framework chapter.

### 3.4 Invocation

- Called from `scripts/build_pdf.sh` *before* LaTeX compilation via a CLI
  entry: `uv run python -m cosmos77_ex03.cli figures` which calls
  `sdk.sdk` → figures façade → `charts.adoption_curve()` and
  `charts.framework_fit()`. Single SDK entry (17 RULES) is respected: the CLI
  does not import `charts` directly.

## 4. TikZ Block Diagram — `tex/figures/diagram_tikz.tex` (B4)

- Satisfies **B4** ("≥1 image — TikZ diagram"). It is a vector image, not a
  raster, so it scales cleanly at the ~15-page layout.
- Depicts the **four-layer production-agent architecture**:
  1. **Planner** (task decomposition / control loop)
  2. **Memory** (short-term context + long-term store / RAG)
  3. **Tools** (function calling, code, external APIs)
  4. **Observability** (tracing, cost meter, evals, governance gates)
- Implementation notes:
  - Pure `tikzpicture` with `\node[draw,rounded corners]` blocks stacked
    vertically, arrows showing the control/data flow Planner → Tools → Memory
    and the cross-cutting Observability lane.
  - Uses only packages already in `tex/preamble.tex` (`tikz`); no external
    libraries beyond `positioning`/`arrows.meta`, which must be declared in the
    preamble via `\usetikzlibrary{...}`.
  - English labels only (Arabic forbidden; this is not the Hebrew chapter).
  - `\input{figures/diagram_tikz}` inside a `figure` float with `\caption` and
    `\label{fig:arch}` so it is cross-referenceable and shows in TOC list of
    figures.

## 5. Comparison Table — `tex/latex/table.tex` (B6)

- Satisfies **B6**: ≥1 non-overflowing table using `tabularx` + `booktabs`.
- Content: framework comparison (rows = LangGraph/CrewAI/AutoGen/LlamaIndex/
  PydanticAI/DSPy; columns = Orchestration model, State/Memory, Tooling,
  Production maturity, Best fit).
- Page-fit strategy:
  - Wrap in `\begin{tabularx}{\textwidth}{@{}lX X X l@{}}` so the wide
    description columns (`X`) absorb slack and the table never exceeds
    `\textwidth`.
  - Rules via `\toprule` / `\midrule` / `\bottomrule` (no vertical rules,
    booktabs convention).
  - Long cell text wraps automatically inside `X` columns — no horizontal
    overflow (the explicit B6 requirement, re-checked by `scripts/qa_pdf.py`).
- Wrapped in a `table` float with `\caption{}` + `\label{tab:frameworks}`.

## 6. Fancy Display Formula — `tex/latex/formula.tex` (B7)

- Satisfies **B7**: ≥1 *fancy* `amsmath` display equation (not flat inline
  text).
- Primary equation — **Total Cost of Ownership** of a production agent:
  ```latex
  \begin{equation}
    \mathrm{TCO} \;=\;
      \underbrace{\sum_{i} u_i\, p_i}_{\text{Usage}}
      \;+\; \underbrace{R_{\text{runtime}}}_{\text{Runtime}}
      \;+\; \underbrace{G}_{\text{Governance}}
      \;+\; \underbrace{O}_{\text{Operations}}
    \label{eq:tco}
  \end{equation}
  ```
- Uses `\underbrace`, `\sum`, `\mathrm`, and `equation` numbering — visually
  "fancy", which `qa_pdf.py` verifies by asserting the presence of an `amsmath`
  display environment rather than a plain text line.
- Optional secondary equation (RAG cosine similarity) may be added in the
  memory chapter using `align` if a second formula is desired; not required for
  B7.

## 7. Integration Into `tex/main.tex`

- `tex/preamble.tex` declares: `graphicx` (for the chart PDFs), `tikz` +
  libraries, `booktabs`, `tabularx`, `amsmath`. `hyperref` stays **last** with
  `unicode=true` (per LaTeX stack canon).
- The article body includes assets via:
  - `\includegraphics[width=\linewidth]{figures/adoption.pdf}` (B5)
  - `\includegraphics[width=.85\linewidth]{figures/frameworks.pdf}` (B5)
  - `\input{figures/diagram_tikz}` (B4)
  - `\input{latex/table}` (B6)
  - `\input{latex/formula}` (B7)
- All four float captions feed the TOC / list of figures-tables (supports B3).

## 8. Build Order

1. `uv run python -m cosmos77_ex03.cli figures` → writes
   `tex/figures/adoption.pdf` and `tex/figures/frameworks.pdf`.
2. `lualatex → biber → lualatex → lualatex` (per canon) consumes the PDFs plus
   the TikZ/table/formula snippets.
3. `scripts/qa_pdf.py` post-checks page count, figure presence, table fit, and
   formula environment (**B15**).

## 9. Testing Strategy (TDD, mocked, ≥85% coverage)

All tests live under `tests/` and run with `uv run pytest`. No live LLM /
CrewAI / lualatex calls (17 RULES); figure tests need none since charts are pure
Python.

| Test | Target | Assertion |
|------|--------|-----------|
| `test_adoption_curve_creates_pdf` | `adoption_curve()` | returns a `Path`; file exists in a **`tmp_path`** dir; size > 0 bytes; valid `%PDF` magic header |
| `test_framework_fit_creates_pdf` | `framework_fit()` | same non-empty PDF checks; one bar per framework |
| `test_charts_are_deterministic` | both functions | two consecutive renders to `tmp_path` produce identical byte length (seeded) |
| `test_figures_dir_from_config` | `figures_dir()` | path resolves from `setup.json`, not a literal string |
| `test_table_snippet_has_environments` | `tex/latex/table.tex` | contains `tabularx`, `\toprule`, `\bottomrule`; no `\hline`/vertical rules |
| `test_formula_snippet_is_amsmath_display` | `tex/latex/formula.tex` | contains `\begin{equation}` (or `align`) and `\underbrace`; not flat text |
| `test_tikz_diagram_has_four_layers` | `tex/figures/diagram_tikz.tex` | contains `tikzpicture` and the four layer labels |

- Tests redirect `figures_dir()` to `tmp_path` via the config fixture so the
  committed `tex/figures/` is never polluted during test runs.
- `ruff` must report zero issues on `charts.py` and helpers (17 RULES).

## 10. Acceptance Mapping Summary

- **B4** — `tex/figures/diagram_tikz.tex` (four-layer TikZ image).
- **B5** — `adoption.pdf` (Gartner projection) + `frameworks.pdf` from
  `charts.py`.
- **B6** — `tex/latex/table.tex` (`tabularx`+`booktabs`, page-fit).
- **B7** — `tex/latex/formula.tex` (`amsmath` display, TCO equation).
- **B1/B3** — assets contribute pages and TOC float entries.
- **B11** — all snippets and generated PDFs committed under `tex/`.
- **B15** — `qa_pdf.py` + unit tests verify correctness (links, fit, env).

## 11. Out of Scope

- LLM-authored figure content, chart styling negotiated by an agent, or any
  CodeInterpreterTool usage (removed from the crew — do not reintroduce).
- Hebrew/BiDi content inside these assets (owned by the dedicated B8 chapter).
- Raster image generation; all images here are vector (TikZ / matplotlib PDF).
