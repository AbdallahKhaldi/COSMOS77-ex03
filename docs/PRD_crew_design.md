# PRD — CrewAI Crew Design: Agents & Task Graph (B10)

## 1. Purpose & Scope

This PRD specifies the CrewAI multi-agent team that researches, plans, writes,
illustrates, edits, and renders the LaTeX source for the article *"AI Agents in
Production: Architecture, Orchestration & Governance in 2026"*. It is the
authoritative design for acceptance criterion **B10** (a real CrewAI
multi-agent team) and the upstream producer for **B11** (the committed,
buildable `tex/` project). It also defines the seams that satisfy **B12**
(provider-agnostic config + Spec Sheet token accounting) and **B13** (CrewAI
Skills wired per agent).

Out of scope here: the LaTeX preamble/stack (its own PRD), the figure-rendering
internals, and the PDF QA checklist (B15). This document stops at the boundary
where the crew emits `output/` artifacts and `tex/sections/*.tex`.

## 2. Design Tenets (binding)

- **No hardcoded config.** Every tunable — model, provider, chapter count,
  `max_rpm`, parallelism — is read from `config/providers.json` and
  `config/setup.json`. Agents NEVER name `gemini/gemini-2.5-flash` inline.
- **Single SDK entry.** The crew is constructed and kicked off only through
  `SDK` in `src/cosmos77_ex03/sdk/sdk.py`. The CLI calls the SDK; nothing else
  touches CrewAI directly.
- **150-line cap.** Agent and task factories are split across multiple files
  (see §7) so no module exceeds the cap.
- **Determinism + mocking.** Every `Crew.kickoff`, every Gemini call, and every
  `lualatex` invocation is mocked in tests. The crew object must be constructible
  and inspectable without a live key.
- **Tokens are always measured.** Usage flows through
  `shared/gatekeeper.py` into the Spec Sheet (B12).

## 3. LLM Binding (provider-agnostic)

All agents share one `LLM` instance built from the active provider in
`config/providers.json` (`active: "gemini"`, model `gemini/gemini-2.5-flash`,
key from env `GEMINI_API_KEY`). A `providers/factory.py` helper resolves the
active block and returns a configured `crewai.LLM`, so swapping to `groq` or
`openai` is a one-line config edit with zero code change. `max_rpm` (from
`setup.json.crew.max_rpm`, currently `10`) is applied at the `Crew` level to
throttle the free tier.

## 4. The Agent Team

One `crewai.Agent` per role. Workers default to `allow_delegation=False` to
prevent cross-talk; only orchestration-capable roles could enable it (none do
in the sequential design). Every agent receives the shared `llm` and a `skills`
list pointing at on-disk Skill folders (B13).

| Agent | role / goal (summary) | tools | skills | allow_delegation |
|-------|----------------------|-------|--------|------------------|
| Researcher | Mine the 2026 source PDF + web for grounded facts and citations | `PDFSearchTool` (on `reference/Agent_Architecture_2026.pdf`), web search tool | `./skills/researcher` | False |
| Outline Planner | Turn research into a 12-chapter `outline.json` with titles, scope, and citation hooks | none (pure reasoning) | `./skills/technical-writer` | False |
| Chapter Writer ×N | Draft one chapter from its outline slice; emit Markdown with citation keys | none | `./skills/technical-writer` | False |
| Figure/Data Agent | Specify the TikZ diagram, the matplotlib graph, and the booktabs table | none (emits specs; rendering is offline) | `./skills/technical-writer` | False |
| Hebrew BiDi Writer | Author exactly one English-primary chapter with an embedded Hebrew–English BiDi section | none | `./skills/technical-writer` | False |
| Editor / Reviewer | Merge chapters into `article.md`, enforce voice, verify citations exist | none | `./skills/technical-writer` | False |
| LaTeX Author | Convert the edited article into `tex/sections/*.tex` + wire figures/tables/bib | none | `./skills/latex-author` | False |

Notes:

- **Researcher** is the only agent with external I/O. Its PDF tool is bound to
  the primary local source `reference/Agent_Architecture_2026.pdf`; the web tool
  is rate-limited by the crew-level `max_rpm`. Both are mocked in tests.
- `CodeInterpreterTool` is **explicitly forbidden** — the matplotlib graph (B5)
  is produced by `scripts/generate_cover_pdf.py`-style offline scripts and the
  Figure/Data Agent only emits the *spec*, never executes code in-crew.
- Chapter Writers are instantiated in a loop: one `Agent` per chapter
  (`num_chapters = 12` from config), each with a stable, indexed role so logs
  and token attribution stay per-chapter.

## 5. The Task Graph

Tasks mirror agents one-to-one except chapters, which fan out. Context wiring
(`Task.context = [...]`) creates the dependency DAG; CrewAI resolves it for a
`Process.sequential` crew. The fan-out chapter tasks set
`async_execution=True` so they run concurrently while the sequential process
guarantees the editor sees all of them before starting.

| # | Task | Agent | depends on (context) | async | output |
|---|------|-------|----------------------|-------|--------|
| T0 | Research | Researcher | — | No | `output/research.md`, `output/citations.json` |
| T1 | Plan outline | Outline Planner | T0 | No | `output/outline.json` |
| T2..T13 | Write chapter NN | Chapter Writer NN | T1 | **Yes** | `output/chapters/ch_NN.md` |
| TB | Write BiDi chapter | Hebrew BiDi Writer | T1 | **Yes** | one `ch_NN.md` (Hebrew slot) |
| TF | Figure/table specs | Figure/Data Agent | T1 | **Yes** | figure/table spec stubs |
| TE | Edit & assemble | Editor / Reviewer | all T2..T13 + TB + TF | No | `output/article.md` |
| TL | Render LaTeX | LaTeX Author | TE | No | `tex/sections/*.tex` |

Dependency rules in prose: **outline depends on research; each chapter depends
on the outline; the editor depends on all chapters; LaTeX depends on the edited
article.** The Hebrew BiDi chapter (B8) and the figure/table specs (B4–B7) are
sibling fan-out tasks gated on the outline and consumed by the editor.

The crew's `tasks=[...]` list is ordered T0, T1, [chapter+bidi+figure async
block], TE, TL. CrewAI runs the list top-to-bottom; the contiguous
`async_execution=True` block is dispatched in parallel and joined before TE,
because TE lists every async task in its `context`.

## 6. ADR-002 — Why `Process.sequential` + async chapters (not hierarchical)

- **Rejected: `Process.hierarchical`.** A manager agent delegating to writers
  introduces a delegation loop: the manager re-asks, writers re-answer, and the
  manager re-evaluates — non-deterministic ping-pong that burns free-tier tokens
  and produces irreproducible runs. It also fights rule 17 (deterministic tests).
- **Chosen: `Process.sequential` with `async_execution=True` chapter tasks.**
  The task list is a fixed, ordered DAG — fully deterministic and trivial to
  mock — yet the chapter-writing stage is genuinely parallel because the async
  tasks are dispatched together and joined at the editor. We get *both*
  determinism *and* parallelism without a manager agent.
- **Consequence:** `allow_delegation=False` on all workers; the "orchestration"
  is the static context wiring, not an LLM. This is the design of record.

## 7. Files & Module Boundaries

All under `src/cosmos77_ex03/crew/`, each under the 150-line cap:

- `agents_research.py` — Researcher + Outline Planner factories.
- `agents_writers.py` — Chapter-Writer loop factory + Figure/Data + Hebrew BiDi.
- `agents_review.py` — Editor/Reviewer + LaTeX Author factories.
- `tasks_research.py` — T0, T1 task builders + context wiring.
- `tasks_chapters.py` — T2..T13, TB, TF async task builders.
- `tasks_assembly.py` — TE, TL task builders + their context lists.
- `crew.py` — assembles agents + tasks into one `Crew(process=Process.sequential,
  max_rpm=<config>)`, exposes `build_crew()` / `kickoff()`; called only by the SDK.

Shared role strings and chapter-status enums live in `constants.py` (no
duplication, rule 3). A `crew/__init__.py` re-exports `build_crew`.

## 8. Throttling the Free Tier

Two config knobs govern concurrency vs. rate:

- `setup.json.crew.parallel_writers` (`true`) — toggles
  `async_execution=True` on the chapter/BiDi/figure block. If set `false`,
  the same tasks fall back to synchronous execution (slower, gentler on quota)
  with **no code change**.
- `setup.json.crew.max_rpm` (`10`) — passed to `Crew(max_rpm=...)`. CrewAI
  enforces a global requests-per-minute ceiling across all agents, so even when
  12 chapter tasks fire in parallel the aggregate Gemini call rate stays under
  the free-tier limit. The async block is about wall-clock latency; `max_rpm`
  is the safety valve that keeps us within quota.

`num_chapters` (`12`) drives both the writer-agent loop and the chapter-task
loop from a single source of truth.

## 9. Token Accounting & Spec Sheet (B12)

After `Crew.kickoff()` returns a `CrewOutput`, the SDK reads
`result.token_usage` (prompt, completion, total, successful requests) and routes
it through `shared/gatekeeper.py`. The gatekeeper records per-run token usage,
latency, and request counts, then writes/updates `output/spec_sheet.json`
(tokens / latency / cost / memory). There is **no hard cap** on the free tier,
but every call is measured. The gatekeeper is the single chokepoint, so a future
paid provider can enforce a budget in one place.

## 10. Acceptance Mapping

| Criterion | How this design satisfies it |
|-----------|------------------------------|
| B4 (TikZ image) | Figure/Data Agent emits the TikZ diagram spec; LaTeX Author embeds it |
| B5 (Python graph) | Figure/Data Agent specs the matplotlib graph; offline script renders to PDF (no CodeInterpreter) |
| B6 (table) | Figure/Data Agent specs a tabularx/booktabs table; LaTeX Author wires it |
| B7 (formula) | Chapter Writers emit amsmath display math; Editor preserves it |
| B8 (BiDi chapter) | Dedicated Hebrew BiDi Writer agent + task TB |
| B9 (bibliography) | Researcher emits `citations.json`; LaTeX Author wires biblatex/biber + hyperref |
| B10 (multi-agent team) | The 7-role crew and DAG in §4–§5 |
| B11 (tex/ builds) | LaTeX Author (TL) writes `tex/sections/*.tex` for the build |
| B12 (config + Spec Sheet) | §3 provider factory + §9 gatekeeper token accounting |
| B13 (Skills) | `skills=[...]` per agent in §4 |

## 11. Testing Strategy (TDD, deterministic)

- Unit-test each agent factory: assert role/goal/`llm`/`skills`/`allow_delegation`
  with the LLM constructor mocked — no live key needed.
- Unit-test the task graph: assert `context` wiring (T1←T0, chapters←T1, TE←all,
  TL←TE) and that the chapter block has `async_execution=True` when
  `parallel_writers` is true.
- Integration-test `build_crew()`: assert `process == Process.sequential`,
  `max_rpm` equals config, and the task count equals `num_chapters + 5`.
- `Crew.kickoff` is mocked to return a stub `CrewOutput` with a known
  `token_usage`; assert the gatekeeper records it into `spec_sheet.json`.
- Seed all randomness; mock every Gemini/web/PDF/subprocess call (rules 6, 17).
