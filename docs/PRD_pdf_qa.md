# PRD — PDF QA Validator: the §13.1 Checklist (B15)

## 1. Purpose & Scope

`scripts/qa_pdf.py` is the **technical-wrapper correctness gate** for HW3. It is the
automated half of acceptance criterion **B15**: it programmatically proves that the
compiled `tex/main.pdf` and its build artifacts satisfy the structural acceptance
criteria **B1–B9** before a human ever opens the PDF. It complements (does not replace)
the **manual eyeball checklist** in §7, which covers the perceptual criteria a grep
cannot judge (RTL rendering, "fancy" formula typesetting, figure aesthetics).

The validator is **read-only**: it never invokes the LLM, CrewAI, or LuaLaTeX. It
inspects files already produced by `scripts/build_pdf.sh`. Consequently it has **no
mocked I/O concern** under the 17 RULES — there is nothing live to mock; tests run it
against static fixtures (§8).

In scope:

- Existence and structural assertions over `tex/main.pdf`, `tex/main.tex`,
  `tex/sections/*.tex`, `tex/figures/*.pdf`, `tex/main.log`, `tex/main.bbl`,
  `tex/main.out`.
- A non-zero exit + a human-readable + machine-readable report on **any** failure.
- A printed manual checklist for the grader.

Out of scope: compiling LaTeX, generating figures, running the crew. Those belong to
`scripts/build_pdf.sh`, `scripts/generate_cover_pdf.py`, and the crew pipeline.

## 2. Design Constraints (17 RULES alignment)

- **150-line cap per `.py`**: `qa_pdf.py` is a thin CLI entry. All check logic lives in
  small modules under `src/cosmos77_ex03/latex/qa/` (one cohesive checker per file),
  re-exported through the single SDK entry `src/cosmos77_ex03/sdk/sdk.py`. No file
  exceeds 150 lines; `scripts/check_line_cap.py` enforces this in CI.
- **Zero hardcoded config**: target page count, tolerances, and required-pattern lists
  come from `config/setup.json` (key `qa`), never literals in code.
- **OOP, no duplication**: a single `Check` dataclass and a `CheckResult` type; each
  assertion is a `Check` subclass / callable registered in a list. The runner iterates
  uniformly — no copy-pasted `if not found: fail(...)` blocks.
- **CLI only**: `uv run python scripts/qa_pdf.py` (or `uv run cosmos77-ex03 qa`).
- **Type hints + docstrings** on every public function/class. **Deterministic tests**,
  coverage **>= 85%**, **ruff** zero, **uv** only.

## 3. Configuration (`config/setup.json`)

```json
{
  "qa": {
    "page_target": 15, "page_tolerance": 3,
    "page_warn_low": 12, "page_warn_high": 18,
    "pdf_path": "tex/main.pdf", "log_path": "tex/main.log",
    "bbl_path": "tex/main.bbl", "out_path": "tex/main.out",
    "tex_root": "tex/main.tex", "sections_glob": "tex/sections/*.tex",
    "figures_glob": "tex/figures/*.pdf",
    "python_figure_stems": ["fig_metrics", "fig_tokens"],
    "report_path": "output/qa_report.json"
  }
}
```

Code reads these via the shared config loader in `src/cosmos77_ex03/shared/`
(e.g. `load_setup()["qa"]`). No key is duplicated as a literal.

## 4. External Tooling

| Tool | Use | Fallback if absent |
|------|-----|--------------------|
| `pdfinfo` (poppler) | page count, PDF validity (B1) | parse `\newlabel`/last page from `.aux`/`.log`; emit WARN, not hard fail |
| Python `re` / file globbing | all `\command` pattern checks | n/a (stdlib) |
| `pathlib` | existence checks | n/a (stdlib) |

`pdfinfo` is the only external binary. Its absence degrades B1 to a warning so the
validator still runs in minimal CI containers; presence is asserted and logged.

## 5. Automated Checks (mapped to B1–B9)

Each row is one registered `Check`. A FAIL appends to the report and forces a non-zero
exit. A WARN is reported but does not fail the run (unless `--strict`).

| ID | Acceptance | What it asserts | Source under test | Severity |
|----|-----------|-----------------|-------------------|----------|
| QA-01 | B1 | `tex/main.pdf` exists and is a valid PDF | `pdfinfo main.pdf` returns 0 | FAIL |
| QA-02 | B1 | page count within `page_target ± page_tolerance`; WARN if `<12` or `>18` | `pdfinfo` "Pages:" | FAIL/WARN |
| QA-03 | B3 | `\tableofcontents` present | `main.tex` | FAIL |
| QA-04 | B3 | running headers/footers configured | `\fancyhead`/`\fancyfoot` + `\pagestyle{fancy}` in `main.tex`/`preamble.tex` | FAIL |
| QA-05 | B4/B5 | at least one `\includegraphics{...}` | `main.tex` + `sections/*.tex` | FAIL |
| QA-06 | B5 | each `python_figure_stems` is `\includegraphics`-included | sections | FAIL |
| QA-07 | B5 | `tex/figures/*.pdf` present (matplotlib output exists on disk) | `figures_glob` | FAIL |
| QA-08 | B6 | a table exists: `\begin{table}` or `tabularx`/`booktabs` (`\toprule`) | sections | FAIL |
| QA-09 | B6 | no `Overfull \hbox` warnings tied to table/figure environments | `main.log` | FAIL |
| QA-10 | B7 | display-math env present: `\begin{equation}`, `\begin{align}`, or `\[ ... \]` | sections | FAIL |
| QA-11 | B9 | at least one `\cite{...}`/`\textcite`/`\parencite` | sections | FAIL |
| QA-12 | B9 | `tex/main.bbl` exists, non-empty, and contains resolved entries (`\entry`/`\bibitem`) | `bbl_path` | FAIL |
| QA-13 | B9 | hyperref produced clickable refs (bookmarks/destinations) | `main.out` non-empty (`\BOOKMARK`) | FAIL |
| QA-14 | B8 | a Hebrew section uses `\foreignlanguage{hebrew}{...}` or `\begin{hebrew}` and contains Hebrew codepoints (U+0590–U+05FF) | sections | FAIL |
| QA-15 | B15 | no Arabic codepoints (U+0600–U+06FF) anywhere in `tex/` | all `.tex` | FAIL |

### 5.1 Check details & rationale

- **QA-02 (B1, ~15 pages)**: Reads the integer after `Pages:` from `pdfinfo`. Hard FAIL
  outside `[target-tol, target+tol]` = `[12, 18]` with default config; the separate
  `page_warn_low/high` give an explicit WARN band so a 13-page draft is flagged loudly
  but does not block iteration. Page count is the single most-weighted structural metric.
- **QA-04 (B3 headers/footers)**: must find BOTH a `\fancyhead`/`\fancyfoot`
  declaration AND an active `\pagestyle{fancy}` (or `\fancypagestyle`), otherwise the
  fancyhdr config is dead code.
- **QA-06 / QA-07 (B5 Python graph)**: two-sided check — the matplotlib PDF must exist
  on disk (QA-07) AND be referenced by an `\includegraphics` (QA-06). A figure that
  exists but is never included, or is included but missing, both FAIL. This is how we
  distinguish the **Python-generated graph (B5)** from the **TikZ diagram (B4)**: B4 is
  satisfied by an inline `tikzpicture` env (QA detects `\begin{tikzpicture}`), B5 by the
  on-disk `tex/figures/*.pdf` from matplotlib.
- **QA-09 (B6 no overflow)**: greps `main.log` for `Overfull \hbox` lines. To avoid
  failing on benign body-text overfulls, the check scopes by correlating the log line's
  reported page/line against the input lines of table/figure environments parsed from
  the sections. Conservative default: any `Overfull \hbox (> 5.0pt too wide)` whose
  nearest preceding environment is a `table`/`tabularx`/`figure` is a FAIL; smaller
  overfulls are WARN. Thresholds live in `config` (`overfull_fail_pt`).
- **QA-12 (B9 bibliography)**: `main.bbl` must exist (proves `biber` ran), be non-empty,
  and contain at least one resolved entry token. An empty `.bbl` means biber failed
  silently — the most common B9 failure.
- **QA-13 (B9 clickable citations)**: presence of `tex/main.out` with `\BOOKMARK`/
  destination entries proves `hyperref` (loaded LAST, `unicode=true`) emitted the PDF
  named destinations that make `\cite` links and TOC entries clickable.
- **QA-14 (B8 BiDi)**: requires the `babel`/`bidi` mechanism (`\foreignlanguage{hebrew}`
  or the `hebrew` environment) **and** actual Hebrew glyphs. Both are needed: Hebrew text
  without `\foreignlanguage` will not render RTL; the markup without text is a stub.
- **QA-15 (B15 / LANGUAGE rule)**: Arabic is forbidden project-wide; this guards the
  canon and catches accidental copy-paste from sources.

## 6. CLI, Report & Exit Semantics

Invocation:

```bash
uv run python scripts/qa_pdf.py            # default: report to stdout + output/qa_report.json
uv run python scripts/qa_pdf.py --strict   # WARN is promoted to FAIL
uv run python scripts/qa_pdf.py --json     # machine-readable only
```

- **Exit code**: `0` only if zero FAILs. Any FAIL -> exit `1`. `--strict` makes WARNs
  also exit `1`.
- **Human report** (stdout): one line per check — `PASS/WARN/FAIL  QA-NN  Bx  <message>`
  — followed by a summary `N passed, M warnings, K failed`.
- **Machine report** (`output/qa_report.json`): list of
  `{id, criterion, status, message, evidence}` objects, where `evidence` carries the
  matched line / page count / file path. This JSON is consumed by the Spec Sheet
  assembly (B12) so QA status is recorded alongside token/latency/cost metrics in
  `output/spec_sheet.json`.

## 7. Manual Eyeball Checklist (printed by `--manual`)

The validator prints this for the grader; these are **B15** judgments a script cannot make:

- [ ] **Cover (B2)** shows topic, author, date, course (203.3763), lecturer (Dr. Yoram Segal).
- [ ] **TOC links (B3/B9)** — clicking a TOC entry jumps to the right chapter.
- [ ] **Hebrew RTL (B8)** — the Hebrew chapter reads right-to-left, punctuation correct,
      English islands inside it read left-to-right.
- [ ] **Table fits (B6)** — no content bleeds into the margin; columns aligned.
- [ ] **Formula is fancy (B7)** — display math is properly typeset, not flat inline text.
- [ ] **Figures render (B4/B5)** — TikZ diagram and matplotlib graph are visible and legible.
- [ ] **Citation click (B9)** — clicking a `\cite` marker jumps to the bibliography entry.

## 8. Testing (TDD, deterministic, mocked external binary)

Per the 17 RULES, tests are deterministic and perform **no live I/O**. `pdfinfo` is the
only external process; it is invoked through a thin `run_pdfinfo()` seam in
`src/cosmos77_ex03/latex/qa/` that tests **mock** to return canned output. All file
inputs are static fixtures.

Fixtures under `tests/fixtures/qa/`:

- `passing/` — a minimal `tex/` tree satisfying every QA-01..QA-15 (valid `main.pdf`
  stub, `main.tex`, one section with table + equation + `\includegraphics` + Hebrew
  `\foreignlanguage`, `main.bbl` with one resolved entry, `main.out` with a `\BOOKMARK`,
  a `figures/fig_metrics.pdf`, a clean `main.log`).
- `failing_missing_table/` — identical to `passing/` but the section's table environment
  is removed.

Test cases (red-green-refactor):

| Test | Expectation |
|------|-------------|
| `test_qa_passes_on_good_fixture` | exit `0`; report all PASS; QA-08 PASS |
| `test_qa_fails_on_missing_table` | exit `1`; report contains `FAIL QA-08 B6`; all other checks still evaluated (no early abort) |
| `test_qa_warns_on_page_count_13` (mocked `pdfinfo` -> 13 pages) | QA-02 WARN, exit `0`; `--strict` -> exit `1` |
| `test_qa_fails_on_empty_bbl` | QA-12 FAIL when `main.bbl` empty |
| `test_qa_fails_on_arabic` | QA-15 FAIL when Arabic codepoint injected |
| `test_report_json_schema` | `output/qa_report.json` has the documented object shape |
| `test_pdfinfo_missing_degrades_to_warn` | mocked `FileNotFoundError` -> QA-01/QA-02 WARN, run completes |

Coverage of the `qa/` package must be **>= 85%**; the runner must evaluate **all**
checks regardless of earlier failures so a single report enumerates every problem.

## 9. Acceptance Criteria Coverage Summary

| Criterion | Covered by |
|-----------|-----------|
| B1 (~15 pages, PDF builds) | QA-01, QA-02 |
| B2 (cover) | manual checklist §7 |
| B3 (TOC + headers/footers) | QA-03, QA-04, QA-13, manual TOC-jump |
| B4 (TikZ image) | QA-05 (`tikzpicture`/`\includegraphics`), manual render |
| B5 (Python graph) | QA-06, QA-07, manual render |
| B6 (non-overflow table) | QA-08, QA-09, manual fit |
| B7 (fancy formula) | QA-10, manual typeset judgment |
| B8 (Hebrew BiDi) | QA-14, manual RTL |
| B9 (clickable citations) | QA-11, QA-12, QA-13, manual citation-jump |
| B12 (Spec Sheet) | `output/qa_report.json` feeds `spec_sheet.json` |
| B15 (technical-wrapper correctness) | the entire validator + manual §7; QA-15 enforces no-Arabic |

## 10. Failure Modes & Decisions (ADR-style)

- `pdfinfo` absence degrades to WARN, not hard error — keeps QA runnable in stripped CI
  while still failing loudly on a grading machine with poppler.
- The runner never short-circuits; it always emits the full multi-check report so the
  author fixes everything in one pass.
- Overfull detection is scoped to table/figure environments (configurable point
  threshold) to avoid noisy false-fails on ordinary justified prose.
- QA reads build artifacts only and is provider/LLM-agnostic — no dependency on
  `config/providers.json`, no tokens emitted — keeping the gate fast, deterministic, and
  free of any mocked-LLM concern.
