# PRD — CrewAI Skills (SKILL.md packages) (B13)

## 1. Purpose & Scope

This PRD specifies the three CrewAI **Skills** that encode the project's
non-negotiable contracts for research, writing, and LaTeX authoring. A Skill is
a folder containing a `SKILL.md` file with YAML frontmatter (a `name` and a
`description` selector) plus a Markdown body of instructions. CrewAI loads the
body into an agent's context **only when relevant**, selected via the
`description` (see <https://docs.crewai.com/en/skills>). Skills are how we move
the graded rules (BiDi LaTeX, house style, citation discipline) out of inline
prompts and into reusable, versioned, testable packages.

This document covers **only the Skills layer** — the `SKILL.md` packages and
their per-agent wiring. It satisfies acceptance criterion **B13 (CrewAI
Skills)** and directly enables **B4–B9, B15** (the LaTeX correctness checklist)
and **B14** (PRD/docs). Agent and task definitions live in the crew PRD; this
PRD references them only at the wiring boundary.

## 2. Deliverables

Three Skill packages under `src/cosmos77_ex03/skills/<name>/SKILL.md`:

| Skill | Folder | Consumed by (agents) | Primary acceptance impact |
|-------|--------|----------------------|---------------------------|
| `researcher` | `skills/researcher/SKILL.md` | researcher | B9 (BibTeX-ready citations), B12 |
| `technical-writer` | `skills/technical-writer/SKILL.md` | all chapter-writers, Hebrew BiDi writer, editor/reviewer | B1 (~15 pp), B3, B7, B9 |
| `latex-author` | `skills/latex-author/SKILL.md` | latex-author | B4–B9, B11, B15 |

Each `SKILL.md` MUST have:
- YAML frontmatter with `name:` (matching the folder name) and a **distinct**
  `description:` selector phrased as "do X; use when Y" so CrewAI's relevance
  matcher fires on the right task.
- A Markdown body that is the agent's operating contract (numbered rules).
- A `metadata:` block (`author: COSMOS77`, `version: "1.0"`) per project
  versioning rule.

Prebuilt drafts exist at `~/COSMOS77/HW3/prebuilt/skills/<name>/SKILL.md` and
SHALL be adapted (not rewritten from scratch) to preserve reviewed wording.

## 3. Skill 1 — `researcher` (source-grounding)

**Frontmatter `description` selector:** "Source-grounding and citation
discipline for technical research. Use when gathering facts that must be backed
by citations."

**Body contract:**
- **Ground every claim**, in priority order: (a) the local primary source
  `reference/Agent_Architecture_2026.pdf`; (b) reputable web (official docs,
  OWASP, Linux Foundation, Gartner, framework docs). Never assert a number or
  quote without a source.
- **Capture each citation as a BibTeX-ready record**: `key` (e.g. `segal2026`),
  author, title, year, venue/publisher, url/doi. Emit as a JSON list the team
  writes to `output/citations.json` and ultimately `tex/refs.bib` — feeds **B9**.
- **Flag the unverifiable** with `[UNVERIFIED]` so writers drop or hedge it;
  never invent sources.
- **Prefer primary over secondary** (cite the OWASP document, not a blog).
- **Output shape:** a list of `{claim, source_key, note}` plus a `citations`
  block, both consumed downstream by writer agents.

**Outputs:** `output/research.md`, `output/citations.json`.

## 4. Skill 2 — `technical-writer` (house style)

**Frontmatter `description` selector:** "House style for clear, cited technical
book/article prose. Use when turning research into chapter text."

**Body contract:**
- **Length budget:** ~1–1.25 pages (~500–650 words) per chapter — keeps the
  article on the ~15-page target (**B1**).
- **One idea per paragraph;** open each chapter with a 1–2 sentence framing.
- **Define on first use** (Harness, RAG, MCP, A2A, observability).
- **Cite ≥1 source per chapter** with an inline `\cite{key}` marker matching
  `refs.bib`; never state a statistic without a citation (feeds **B9**).
- **Voice:** active, precise, engineering-grade — no marketing fluff, no hedging.
- **Terminology consistency** across chapters; one canonical term per concept.
- **Bridge sentence** ends each chapter, linking to the next (supports the
  continuous-narrative structure behind **B3**).
- **Output Markdown** (single `#`/`##` heading) with `\cite{...}` markers only —
  it does **not** emit LaTeX; that is the latex-author skill's job.

**Outputs:** `output/chapters/ch_NN.md`, then assembled `output/article.md`.

## 5. Skill 3 — `latex-author` (BiDi LaTeX contract)

**Frontmatter `description` selector:** "Convert Markdown to clean, compiling
LuaLaTeX with correct BiDi, fancy math, non-overflow tables, and linked
citations. Use when producing .tex from finished content."

**Body contract — this is the graded LaTeX checklist:**
- **Emit ONLY valid LuaLaTeX** — no prose, no "Here is the LaTeX:" wrapper.
  Output is written verbatim to a `.tex` file under `tex/sections/`.
- **Engine & preamble:** target LuaLaTeX with the project `tex/preamble.tex`:
  `babel[bidi=basic, layout=tabular, english, hebrew]`, `\babelfont`,
  `amsmath`, `booktabs`, `tabularx`, `graphicx`, `tikz`, `fancyhdr`,
  `biblatex` (backend=biber), `hyperref` loaded **last** with `unicode=true`.
- **Fancy math, never flat text** — `equation`/`align`, never plain characters
  (**B7**).
- **Tables never overflow** — `tabularx` with an `X` column + `booktabs`
  rules (`\toprule/\midrule/\bottomrule`); never `\hline`, never fixed-width
  `tabular` past `\linewidth` (**B6**).
- **Figures** via `\includegraphics[width=0.8\linewidth]{figures/<name>.pdf}`
  inside a `figure` env with `\caption` + `\label` — covers the TikZ diagram
  (**B4**) and the matplotlib-generated PDF graph (**B5**).
- **Citations:** every `\cite{key}` matches a key in `tex/refs.bib`;
  `\printbibliography` at the end; `hyperref` makes cites/refs clickable (**B9**).
- **BiDi (Hebrew chapter):** wrap inline English runs with
  `\foreignlanguage{english}{...}`; anchor trailing direction with `\rlm`; let
  `bidi=basic` mirror parentheses; rely on `layout=tabular` for table
  direction; switch with `\selectlanguage{hebrew}` / `\selectlanguage{english}`
  (**B8**). Arabic is forbidden anywhere.
- **Structure:** `\section`/`\subsection` only; never redefine the preamble
  inside a fragment.
- **Compile awareness:** the document builds `lualatex → biber → lualatex →
  lualatex` (4 passes); produce LaTeX that resolves with zero undefined
  references — directly underwrites **B11** and **B15**.

**Outputs:** `tex/sections/*.tex` fragments assembled by `tex/main.tex`.

## 6. Per-Agent Wiring (CrewAI 1.x)

Skills attach to agents via the `skills` parameter, given as **relative paths
to the skill folder** (CrewAI resolves and loads the `SKILL.md`), per
<https://docs.crewai.com/en/skills>:

```python
researcher = Agent(..., skills=["./skills/researcher"])
chapter_writer = Agent(..., skills=["./skills/technical-writer"])
hebrew_writer = Agent(..., skills=["./skills/technical-writer"])
editor = Agent(..., skills=["./skills/technical-writer"])
latex_author = Agent(..., skills=["./skills/latex-author"])
```

| Agent | Skill(s) | Rationale |
|-------|----------|-----------|
| researcher | `./skills/researcher` | citation discipline, source priority |
| outline-planner | — | no Skill (structure planning only) |
| chapter-writers (per chapter) | `./skills/technical-writer` | house style + length budget |
| figure/data agent | — | emits matplotlib PDF; LaTeX handled by latex-author |
| Hebrew BiDi writer | `./skills/technical-writer` | same house style; BiDi handled at latex stage |
| editor/reviewer | `./skills/technical-writer` | enforces style consistency |
| latex-author | `./skills/latex-author` | the BiDi LaTeX contract |

Paths are resolved relative to the crew working directory; the crew factory
runs from `src/cosmos77_ex03/`, so `./skills/<name>` maps to
`src/cosmos77_ex03/skills/<name>/`. Paths are read from config, never
hardcoded inline, consistent with the zero-hardcoded-config rule.

## 7. Constraints & Rules Compliance

- **17 RULES:** `SKILL.md` files are Markdown, not Python, so the 150-line
  `.py` cap does not gate them; however the line-cap script
  (`scripts/check_line_cap.py`) only scans `.py`. Skill bodies stay focused and
  English-only. No secrets appear in any `SKILL.md`.
- **No hardcoded model:** Skills describe behavior, never name a model; the LLM
  (`gemini/gemini-2.5-flash`) comes from `config/providers.json`.
- **OOP / no duplication:** the shared `technical-writer` Skill is wired to four
  agents rather than duplicating prose in each agent's `backstory`.
- **Versioning 1.00** recorded in each `SKILL.md` `metadata.version`.

## 8. Testing Strategy (TDD, deterministic, mocked)

All LLM/CrewAI I/O is mocked — Skills are validated by structure and wiring,
never by live calls:
- **Frontmatter validity:** parse each `SKILL.md`; assert `name` matches its
  folder, `description` is non-empty and **unique** across the three Skills.
- **Body content checks:** assert each contract's load-bearing tokens are
  present (e.g. `tabularx` + `\foreignlanguage` in latex-author; `\cite` in
  technical-writer; `[UNVERIFIED]` in researcher).
- **Wiring:** assert each Agent is constructed with the expected
  `skills=[...]` list (mock the `Agent` constructor; inspect kwargs).
- **Determinism & coverage:** tests are pure file/string assertions, fully
  deterministic; the Skills loader/wiring module contributes to the
  project-wide **≥85% coverage** target. `ruff` reports zero.

## 9. Acceptance Mapping (B13 + dependents)

| Criterion | How Skills satisfy it |
|-----------|------------------------|
| **B13** | Three real `SKILL.md` packages wired via `skills=[...]` |
| **B4/B5** | latex-author figure rules (`\includegraphics`, TikZ, matplotlib PDF) |
| **B6** | latex-author `tabularx`+`booktabs` non-overflow rule |
| **B7** | latex-author fancy-math rule (`equation`/`align`) |
| **B8** | latex-author BiDi rule (`\foreignlanguage`, `\selectlanguage`) |
| **B9** | researcher BibTeX records + latex-author `\cite`/`\printbibliography` |
| **B1/B3** | technical-writer length budget + chapter framing/bridges |
| **B11/B15** | latex-author 4-pass-safe output, zero undefined refs |
| **B14** | this PRD (`docs/PRD_skills.md`) |
