# PRD — Research & Web-Search Tooling

## 1. Purpose & Scope

This PRD specifies the **research and web-search tooling** layer of COSMOS77-ex03
(package `cosmos77_ex03`), the toolset that feeds verified, citable source
material to the CrewAI multi-agent team producing the ~15-page LaTeX article
*"AI Agents in Production: Architecture, Orchestration & Governance in 2026"*.

The tooling lives in a single module, **`src/cosmos77_ex03/crew/tools.py`**, and
exposes:

1. A **web-search capability** that degrades gracefully across three tiers
   (SerperDev → scrape/website-search → local PDF reader).
2. A **citation-capture pipeline** that turns every factual claim into a
   BibTeX-ready record persisted to `output/citations.json`.
3. A **file-writing capability** (`FileWriterTool`) for emitting `.md` and
   `.tex` artifacts under `output/` and `tex/`.

The module is the upstream dependency for the `researcher` agent and the
`latex-author` agent; its correctness directly determines **B9** (bibliography
with clickable, resolved citations) and underpins the source quality behind the
article body (B1–B8).

## 2. Goals & Non-Goals

### Goals
- Provider-agnostic, env-driven tool selection — **zero hardcoded keys or URLs**
  (config in `config/*.json` / `.env`; secrets only via env vars).
- Deterministic, fully **mocked** behavior under test (no live HTTP, no live
  Serper, no live LLM) — satisfies the TDD + "deterministic tests" rules.
- Every claim → exactly one citation record; no orphan claims, no orphan keys.
- Keep `tools.py` under the **150-line hard cap**; split helpers into
  `crew/citations.py` and `crew/tool_select.py` if the cap is approached.

### Non-Goals
- No autonomous browsing/crawling beyond a fixed allow-list of reputable
  domains.
- No `CodeInterpreterTool` (removed from the design — must not be referenced).
- No live network in CI; live calls are an opt-in manual smoke path only.

## 3. Tool Inventory & Selection Logic

### 3.1 Selection function

A single pure function decides the available tool set from the environment so
that selection is testable in isolation:

```python
def select_research_tools(env: Mapping[str, str]) -> ResearchToolset:
    """Return the research toolset available for the current environment.

    Tier 1: SerperDevTool when env['SERPER_API_KEY'] is set.
    Tier 2: ScrapeWebsiteTool + WebsiteSearchTool over the reputable allow-list.
    Tier 3 (always present): LocalPdfReaderTool over the local reference PDF.
    """
```

- `select_research_tools` reads **only** the injected `env` mapping (default
  `os.environ`) so tests pass a fake dict — **deterministic**, no monkeypatching
  of the network.
- It returns a frozen `ResearchToolset` dataclass: `search_tools: list[BaseTool]`,
  `pdf_tool: BaseTool`, `writer_tool: BaseTool`, `citation_tool: BaseTool`,
  `tier: str`.
- The allow-list of reputable sources and the reference PDF path are read from
  `config/setup.json` (extend with a `research` block:
  `reputable_sources: [...]`, `reference_pdf: "reference/Agent_Architecture_2026.pdf"`).

### 3.2 Fallback tiers

| Tier | Trigger condition | Tools enabled | CrewAI 1.x class | Notes |
|------|-------------------|---------------|------------------|-------|
| 1 — API search | `SERPER_API_KEY` present | Live keyword search | `crewai_tools.SerperDevTool` | Highest recall; key via env only |
| 2 — Open web | No Serper key | Targeted scrape + RAG search over allow-list | `crewai_tools.ScrapeWebsiteTool`, `crewai_tools.WebsiteSearchTool` | Bounded to reputable domains |
| 3 — Local (always on) | Always available | Read/RAG over `reference/Agent_Architecture_2026.pdf` | `crewai_tools.PDFSearchTool` (wrapped as `LocalPdfReaderTool`) | The primary local source; guarantees offline determinism |

Tiers are **additive within their tier ceiling**: Tier 3 is always appended so
the crew can run with no network access at all (required for offline CI and the
guaranteed-source path behind every chapter).

### 3.3 File writer

- `FileWriterTool` (`crewai_tools.FileWriterTool`) is wired for writing `.md`
  (chapter drafts → `output/chapters/ch_NN.md`, `output/article.md`,
  `output/research.md`) and `.tex` (sections → `tex/sections/`).
- Path roots come from `config/setup.json#paths` (`output_dir`, `tex_dir`,
  `figures_dir`) — never hardcoded. A guard rejects writes outside those roots.

## 4. Citation Capture Pipeline (B9)

### 4.1 Data contract

Every factual claim used in the article MUST resolve to a citation record in
`output/citations.json`. Record schema (BibTeX-ready):

```json
{
  "key":    "agentarch2026",        // unique BibTeX cite key (slug)
  "author": "Author, A. and Author, B.",
  "title":  "Agent Architecture in 2026",
  "year":   "2026",
  "url":    "https://example.org/...",
  "source_tier": "local|web|serper",
  "claim":  "verbatim claim text the citation supports"
}
```

- `citations.json` is a JSON object: `{"version": "1.00", "items": [ ... ]}`.
- Cite keys are deterministic slugs (`author-year-titlehash`), de-duplicated;
  re-running the crew is idempotent (same input → same keys).
- A `CitationCaptureTool` (custom `BaseTool` subclass) is the only writer of
  `citations.json`. The `latex-author` agent reads it to emit `tex/refs.bib`
  via a `to_bibtex(items) -> str` helper, ensuring every `\cite{key}` in the
  body has a matching `@article/@misc` entry.

### 4.2 Flow

1. Researcher agent invokes a search/PDF tool → gets passages + URLs/metadata.
2. For each extracted claim, the agent calls `CitationCaptureTool` with the
   claim text and the source metadata → appends a validated record.
3. `latex-author` renders `refs.bib` from `citations.json`; biblatex+biber +
   hyperref produce **clickable, resolved** citations.
4. `scripts/qa_pdf.py` cross-checks: every `\cite` key exists in `refs.bib`
   and every `refs.bib` entry is cited — this is the B9 / B15 gate.

### 4.3 Validation rules
- Reject records missing any of `key/author/title/year/url`.
- Reject duplicate keys (merge claims under the existing key instead).
- `url` must be syntactically valid; `year` is a 4-digit string.
- Local-PDF citations use the canonical metadata of
  `reference/Agent_Architecture_2026.pdf` with a stable `key` and a
  `file://`-style or repository-relative `url`.

## 5. CrewAI Wiring

- Tools are attached per agent in the crew assembly (`crew/agents.py` /
  `crew/crew.py`): the `researcher` agent receives
  `toolset.search_tools + [toolset.pdf_tool, toolset.citation_tool]`; the
  `latex-author` agent receives `[toolset.writer_tool]`.
- The `researcher` agent also loads the `researcher` skill
  (`skills=["./skills/researcher"]`) for selection/quality guidance; tool use
  and skill guidance are complementary (B13).
- Process is **`Process.sequential`** with `async_execution=True` on chapter
  tasks; `allow_delegation=False` for workers (per ADR-002). The research tool
  layer is provider-agnostic and never references the active LLM model
  (`gemini/gemini-2.5-flash`) directly — the model is resolved only through
  `config/providers.json` (`active` + per-provider `model`/`api_key_env`).

## 6. Configuration Keys

| Key | File | Purpose |
|-----|------|---------|
| `SERPER_API_KEY` | `.env` (gitignored) | Tier-1 search toggle + auth |
| `research.reputable_sources` | `config/setup.json` | Tier-2 domain allow-list |
| `research.reference_pdf` | `config/setup.json` | Tier-3 local PDF path |
| `paths.output_dir` / `paths.tex_dir` / `paths.figures_dir` | `config/setup.json` | Writer roots |
| `crew.require_citation_per_chapter` | `config/setup.json` | Enforce ≥1 citation per chapter |
| `active` / `providers.*` | `config/providers.json` | LLM provider (never hardcoded) |

## 7. Testing Strategy (TDD, mocked, ≥85% coverage)

- **`select_research_tools`**: table-driven tests over fake `env` dicts assert
  the correct tier and tool composition (Serper present, Serper absent,
  empty env → Tier 3 only).
- **Network is never live**: `SerperDevTool`, `ScrapeWebsiteTool`,
  `WebsiteSearchTool`, and `PDFSearchTool` are replaced with fakes returning
  fixed fixtures. No live LLM/CrewAI/Gemini/lualatex I/O in any test.
- **`CitationCaptureTool`**: tests cover append, de-dup, idempotency, schema
  rejection, and round-trip to BibTeX (`to_bibtex` output parses).
- **`FileWriterTool` guard**: writes outside configured roots raise.
- All tests deterministic; ruff must report **zero**; line cap enforced by
  `scripts/check_line_cap.py`.

## 8. Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Serper quota/key absence breaks runs | Always-on Tier 3 local PDF reader guarantees a source |
| Hallucinated/unresolved citations | `qa_pdf.py` cross-check fails the build (B9/B15) |
| `tools.py` exceeds 150 lines | Split into `crew/citations.py` + `crew/tool_select.py` |
| Network flakiness in CI | All search/PDF tools mocked; offline path is the default |
| Non-reputable sources cited | Tier-2 bounded to `research.reputable_sources` allow-list |

## 9. Acceptance Mapping

- **B9** — citations exist and resolve: §4 pipeline + `qa_pdf.py` gate.
- **B10** — real CrewAI team: §5 per-agent tool wiring under
  `Process.sequential`.
- **B11/B14** — `tex/` builds, docs present: writer outputs feed `tex/`; this
  PRD is a `docs/` artifact.
- **B12** — provider-agnostic config + Spec Sheet: §6 keys, no hardcoded model;
  token usage recorded via `result.token_usage` into `output/spec_sheet.json`.
- **B13** — Skills: `researcher` skill bound to the researcher agent.
- **B15** — technical correctness: §4.2 / §7 ensure links resolve and every
  citation has a matching BibTeX entry.

## 10. Deliverables

- `src/cosmos77_ex03/crew/tools.py` — `select_research_tools`,
  `ResearchToolset`, `CitationCaptureTool`, `LocalPdfReaderTool` wrapper,
  `FileWriterTool` wiring (split into `crew/citations.py` /
  `crew/tool_select.py` if the line cap requires).
- `output/citations.json` — populated, validated citation store.
- Test suite achieving ≥85% coverage with all external I/O mocked.
