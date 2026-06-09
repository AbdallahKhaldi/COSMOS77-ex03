# PRD — COSMOS77-ex03 (HW3: CrewAI + LaTeX Article Generator)

## 1. Context

203.3763 HW3 ("Article/Book Generation with CrewAI and LaTeX", Dr. Yoram Segal) asks
us to operationalize the central thesis of Lecture 06: the gap between a Proof-of-Concept
agent demo and a **production** multi-agent system. A PoC can prompt one LLM and paste the
answer; production demands orchestration, deterministic execution, governance, cost
accounting, and a reproducible artifact. This project answers that thesis by *being* a
production-shaped pipeline rather than merely describing one.

- A **CrewAI 1.x multi-agent team** performs the knowledge work: research, outline,
  parallel chapter authoring, figures/data, a Hebrew BiDi chapter, editorial review, and
  LaTeX assembly. This demonstrates orchestration, role specialization, and delegation
  control — the architecture/orchestration/governance triad of the article's own title.
- A **LaTeX pipeline** (LuaLaTeX + biber) compiles the crew's Markdown/JSON outputs into a
  ~15-page PDF. The compiled `tex/main.pdf` is the heart of the grade (B1–B11, B15).
- The article topic — *"AI Agents in Production: Architecture, Orchestration & Governance
  in 2026"* — is deliberately the same problem space the system embodies, so the deliverable
  is self-referential evidence that we understood the lecture.

The end-to-end contract is a single command, `cosmos77-article run`, that goes from prompt
to compiled PDF with a measurable **Spec Sheet** (tokens, latency, cost, memory) proving the
system is observable and governable, not a black box.

## 2. Stakeholders

| Stakeholder | Role | Primary interest |
|---|---|---|
| Dr. Yoram Segal (lecturer) | Author of the assignment & rubric | The PoC→Production thesis is demonstrated; canon and acceptance criteria honored |
| The grader (technical wrapper) | Evaluates the deliverable | `uv sync` then build reproduces `tex/main.pdf`; links resolve, citations exist, BiDi correct, tables fit, formulas are typeset (B15) |
| Abdallah Khaldi (partner) | Engineer/author | Crew, providers, SDK, LaTeX stack land cleanly under the 17 rules |
| Tasneem Natour (partner) | Engineer/author | Skills, figures, tests/coverage, docs, commit hygiene land cleanly |

Authorship: commits credit the two students only; conventional-commit messages reference
TODO IDs. The grader is the hardest stakeholder — every functional requirement below maps
to something they can mechanically verify.

## 3. User Stories

- **As a user**, I run one command — `cosmos77-article run` — and a CrewAI crew researches
  the topic, writes the chapters in parallel, generates figures, writes the Hebrew BiDi
  chapter, reviews the draft, and compiles a ~15-page PDF. (B1, B10)
- **As the grader**, I run `uv sync` and `scripts/build_pdf.sh` and a byte-stable PDF appears
  at `tex/main.pdf` without any live network/LLM call required for the build step. (B11)
- **As an architect**, I switch the LLM from Gemini to Groq or OpenAI by editing one key in
  `config/providers.json` — no code changes, nothing hardcoded. (B12)
- **As a reviewer**, I open `output/spec_sheet.json` and see per-run tokens, latency, cost,
  and peak memory recorded by the gatekeeper cost meter. (B12)
- **As a developer**, I run the test suite offline — every LLM/CrewAI/Gemini/LuaLaTeX I/O
  is mocked — and see coverage ≥ 85% and ruff reporting zero issues.
- **As a reader**, I open the PDF and find a cover, TOC, running headers/footers, a TikZ
  diagram, a matplotlib graph, a non-overflowing table, a display formula, one Hebrew-English
  chapter, and clickable resolved citations. (B2–B9, B15)

## 4. Functional Requirements (mapped to B1–B15)

| ID | Requirement | Implementation anchor | Accept. |
|---|---|---|---|
| FR-01 | Compile a ~15-page article PDF | `scripts/build_pdf.sh` → `tex/main.tex` → `tex/main.pdf` | B1 |
| FR-02 | Cover page (topic, author, date, course, lecturer) | `scripts/generate_cover_pdf.py`, `tex/sections/` titlepage | B2 |
| FR-03 | TOC + chapters + running headers/footers | `\tableofcontents`, `fancyhdr` in `tex/preamble.tex` | B3 |
| FR-04 | ≥1 image as a TikZ diagram | `tikz` block in `tex/figures/` | B4 |
| FR-05 | ≥1 Python-generated graph | figure agent → `src/cosmos77_ex03/figures/` (matplotlib → PDF) | B5 |
| FR-06 | ≥1 non-overflow table | `booktabs`+`tabularx` in `tex/sections/` | B6 |
| FR-07 | ≥1 fancy display formula | `amsmath` display env (not flat text) | B7 |
| FR-08 | One Hebrew-English BiDi chapter | Hebrew BiDi writer agent → `babel(bidi=basic)` + `\babelfont` | B8 |
| FR-09 | Bibliography with clickable resolved citations | `biblatex`(backend=biber) + `\addbibresource{refs.bib}` + `hyperref` | B9 |
| FR-10 | Real CrewAI multi-agent team | `src/cosmos77_ex03/crew/` agents + `Process.sequential`, async chapter tasks | B10 |
| FR-11 | `tex/` project committed and builds | `tex/{preamble.tex,main.tex,sections/,figures/,refs.bib}` | B11 |
| FR-12 | Provider-agnostic config + Spec Sheet | `config/providers.json`, gatekeeper cost meter → `output/spec_sheet.json` | B12 |
| FR-13 | CrewAI Skills wired per agent | `src/cosmos77_ex03/skills/{latex-author,technical-writer,researcher}/SKILL.md` | B13 |
| FR-14 | Project docs present | `docs/{PRD.md,PLAN.md,TODO.md}` + `README.md` | B14 |
| FR-15 | Technical-wrapper correctness | `scripts/qa_pdf.py` asserts links resolve, citations exist, BiDi & tables OK | B15 |

### Crew design (FR-10 detail)

- Agents (one `Agent` each): `researcher`, `outline-planner`, parallel **chapter-writers**
  (one `Agent` per chapter), `figure/data` agent, `hebrew-bidi` writer, `editor/reviewer`,
  `latex-author`.
- Process is **`Process.sequential`** with `async_execution=True` on the chapter-writing
  `Task`s. This is ADR-002: hierarchical risks delegation ping-pong; sequential + async is
  both deterministic and parallel. `allow_delegation=False` for worker agents.
- Token usage is read from `result.token_usage` and fed to the cost meter.
- `CodeInterpreterTool` is **not used** (removed). Skills are wired via
  `skills=["./skills/<name>"]`.

### LLM / config (FR-12 detail)

- Active model: `gemini/gemini-2.5-flash` (free tier), selected via `config/providers.json`
  (`active` provider, per-provider `model` + `api_key_env`). Groq/OpenAI are swappable. The
  model id is **never** hardcoded in Python.
- Secrets live only in `.env` (gitignored); the repo holds no API keys.

### Outputs

- `output/research.md`, `output/outline.json`, `output/chapters/ch_NN.md`,
  `output/article.md`, `output/citations.json`, `output/spec_sheet.json`.
- Primary local source: `reference/Agent_Architecture_2026.pdf`.

## 5. Non-Functional Requirements

- **Modularity / provider-agnostic.** All LLM access flows through the single SDK entry
  `src/cosmos77_ex03/sdk/sdk.py`, configured from `config/providers.json`. OOP with no
  duplication; zero hardcoded config (everything in `config/*.json` or `.env`). Every `.py`
  file is ≤ 150 lines — split larger modules.
- **Reproducibility.** `uv` only. The grader runs `uv sync` and `scripts/build_pdf.sh`
  (`lualatex → biber → lualatex → lualatex`) to rebuild `tex/main.pdf`. Tests are
  deterministic; **all** LLM/CrewAI/Gemini/LuaLaTeX I/O is mocked — no live calls in tests.
- **Measurability.** The gatekeeper cost meter records tokens/latency/cost/memory into
  `output/spec_sheet.json` for every run. A prompt log is kept per session.
- **Quality gates.** Test coverage ≥ 85%; `ruff` reports zero issues; public surfaces carry
  docstrings + type hints; `scripts/check_line_cap.py` enforces the 150-line cap; TDD
  red-green-refactor throughout; versioning starts at 1.00.
- **Language.** All code and docs are English. The article is English-primary with **exactly
  one** Hebrew-English BiDi chapter. **Arabic is forbidden anywhere** in the repo or PDF.
- **Interface.** CLI only (`cosmos77-article`), no GUI.

## 6. KPIs / Definition of Done

- Compiled `tex/main.pdf` is ~15 pages with cover, TOC, and running headers/footers.
- ≥1 TikZ image, ≥1 matplotlib graph, ≥1 non-overflowing table, ≥1 display formula.
- Exactly one Hebrew-English BiDi chapter renders correctly (no Arabic anywhere).
- Bibliography present with clickable, resolved `biblatex`/`biber` citations.
- Test coverage ≥ 85%; `ruff` = 0 findings; line-cap script passes.
- ≥ 600 TODO items tracked in `docs/TODO.md`, each referenced by conventional commits.
- `output/spec_sheet.json` populated with tokens, latency, cost, and memory.
- `uv sync` + build reproduces the PDF on the grader's machine.

## 7. Out of Scope

- Any graphical user interface — the deliverable is strictly CLI-driven.
- Languages beyond English and the single Hebrew BiDi chapter (no Arabic, no others).
- Model fine-tuning or training — we consume hosted models via the provider config only.
- Live LLM/LaTeX calls inside the test suite — those paths are always mocked.
- Hierarchical CrewAI orchestration and `CodeInterpreterTool` — explicitly rejected (ADR-002).
