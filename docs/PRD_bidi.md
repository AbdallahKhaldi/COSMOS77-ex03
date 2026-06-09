# PRD — Hebrew-English BiDi Chapter (B8)

## 1. Purpose & Scope

This PRD specifies the single Hebrew-English bidirectional (BiDi) chapter required
by acceptance criterion **B8** of HW3 ("AI Agents in Production: Architecture,
Orchestration & Governance in 2026"). The article is English-primary and contains
**exactly one** BiDi chapter whose body language is Hebrew (RTL) with English
technical terms (LTR) interleaved inline. Arabic is forbidden anywhere in the
deliverable.

The chapter must render correctly in the compiled `tex/main.pdf` and pass the
technical-wrapper checks of **B15** (BiDi correct: no reversed runs, no missing
glyphs, no punctuation drift, tables keep column order).

In scope:
- The LaTeX BiDi mechanism (babel `bidi=basic`, `\foreignlanguage`, `\rlm`,
  `layout=tabular`, `\selectlanguage`).
- The CrewAI `bidi_writer` agent that authors the Hebrew body.
- Font fallback so every Hebrew glyph resolves.
- A QA gate that proves correctness for B15.

Out of scope: the other chapters (English LTR), the bibliography mechanics (B9),
and the figure/table generation pipeline except where a table or formula lives
inside the BiDi chapter.

## 2. Deliverables & File Map

| Artifact | Path | Role |
|---|---|---|
| BiDi chapter source | `tex/sections/ch_bidi.tex` | The compiled Hebrew-English chapter (LTR + RTL runs) |
| BiDi chapter draft | `output/chapters/ch_NN.md` | Markdown draft emitted by the `bidi_writer` agent |
| Preamble (BiDi stack) | `tex/preamble.tex` | babel/fontspec/`\babelfont` setup shared by the whole document |
| BiDi writer agent | `src/cosmos77_ex03/crew/agents.py` | Defines the `bidi_writer` CrewAI Agent |
| BiDi writer task | `src/cosmos77_ex03/crew/tasks.py` | The async chapter task that produces the Hebrew body |
| Hebrew-aware skill | `src/cosmos77_ex03/skills/technical-writer/SKILL.md` | Selector + guidance for BiDi authoring |
| BiDi QA check | `scripts/qa_pdf.py` | Asserts BiDi correctness for B15 |
| Provider config | `config/providers.json` | Active LLM provider/model (never hardcoded) |

## 3. How RTL ↔ LTR Is Handled

The document language stack lives in `tex/preamble.tex`. English is the **main**
language; Hebrew is a secondary language. We rely on the LuaTeX-native Unicode
BiDi algorithm rather than any external RTL package.

### 3.1 Preamble configuration

```latex
\usepackage[bidi=basic, layout=tabular, english, hebrew]{babel}
\babelprovide[import]{hebrew}
\babelfont{rm}{FreeSerif}                       % Latin + Hebrew coverage
\babelfont[hebrew]{rm}{Culmus David CLM}         % Hebrew-specific face
% macOS fallback when Culmus is unavailable: Arial Hebrew
```

- `bidi=basic` enables LuaTeX's native Unicode BiDi engine. It reorders mixed
  runs per the UAX#9 algorithm and **mirrors paired punctuation automatically**
  (parentheses, brackets, angle brackets) — we never flip these by hand.
- `layout=tabular` keeps RTL **tables** in logical (left-to-right) column order,
  so a `tabularx`/`booktabs` table authored inside the Hebrew chapter renders
  with its first column on the correct side (supports B6 inside a BiDi context).
- English (`english`) is declared first so it is the main/default direction.

### 3.2 Block-level switching

The chapter body is wrapped so its default direction is RTL:

```latex
\selectlanguage{hebrew}
... Hebrew paragraphs ...
\selectlanguage{english}
```

`\selectlanguage` sets paragraph direction and the active font for whole blocks
(headings, paragraphs, list bodies). Use it at chapter scope and to return to
English at the chapter boundary so the next (English) chapter is unaffected.

### 3.3 Inline English runs inside Hebrew

For LTR technical terms embedded in an RTL sentence (e.g. "orchestration",
"CrewAI", "LuaLaTeX"), wrap each run:

```latex
... ה־\foreignlanguage{english}{orchestration} מבוצע על ידי ...
```

`\foreignlanguage{english}{...}` switches direction and font for the span only,
without resetting the surrounding paragraph. This is the primary tool for
"Hebrew body with English technical terms inline" and is what the `bidi_writer`
agent emits for every Latin token.

### 3.4 Anchoring trailing direction with `\rlm`

When an RTL run **ends** with neutral characters (a period, comma, or closing
parenthesis after an English term), the BiDi algorithm can attach that neutral
to the wrong direction, causing visible drift. Insert a `\rlm` (Right-to-Left
Mark) to anchor the trailing direction back to RTL:

```latex
... \foreignlanguage{english}{governance}\rlm.
```

## 4. Pitfalls & Mitigations

| Pitfall | Symptom in PDF | Mitigation |
|---|---|---|
| Digit direction | Numbers in an RTL run drift or reorder | Keep numerals inside `\foreignlanguage{english}{...}`; numbers stay LTR (correct) |
| Bracket/paren mirroring | `(` and `)` appear swapped | None needed — `bidi=basic` mirrors paired punctuation automatically |
| End-of-line punctuation drift | A `.` or `,` jumps to the wrong line end | Anchor with `\rlm` after the neutral; never end an English run with bare punctuation |
| English fragment breaks mid-line | A term splits across the RTL/LTR boundary | Wrap the whole term in one `\foreignlanguage{english}{...}` (a single non-breaking run) |
| Empty boxes / `.notdef` | Hebrew glyphs render as blank boxes | Font fallback: `\babelfont[hebrew]{rm}{Culmus David CLM}`, FreeSerif primary, Arial Hebrew on macOS |
| RTL table column reversal | First column appears on the wrong side | `layout=tabular` in the babel options preserves logical column order |
| `hyperref` ordering | Broken links / direction state leaks | Load `hyperref` **last** with `unicode=true` (matches the LATEX STACK canon) |

### Font fallback policy

The Hebrew face must cover the full Hebrew block plus niqqud if used. Resolution
order: **FreeSerif** (Latin + Hebrew), then **Culmus David CLM** as the dedicated
Hebrew face, then **Arial Hebrew** as the macOS system fallback. If a glyph is
missing in all three, `qa_pdf.py` flags it (see §6). This directly prevents the
empty-box failure mode that would fail B15.

## 5. The `bidi_writer` Agent (B10, B13)

The Hebrew BiDi chapter is authored by a dedicated CrewAI 1.x Agent, distinct
from the English chapter-writers, defined in
`src/cosmos77_ex03/crew/agents.py`.

- **Role/goal:** write the assigned chapter body in Hebrew, keeping English
  technical terms inline and wrapping each in `\foreignlanguage{english}{...}`.
- **`allow_delegation=False`** (worker default per the crew canon — no delegation
  ping-pong).
- **Skill wiring (B13):** `skills=["./skills/technical-writer"]`; the SKILL.md
  frontmatter `name`/`description` selector guides the agent to BiDi-aware
  output (RTL body, LTR terms, `\rlm` anchoring rules).
- **LLM:** resolved from `config/providers.json` (active provider + per-provider
  model + `api_key_env`); the model id is **never** hardcoded (default
  `gemini/gemini-2.5-flash`).
- **Execution:** the chapter task runs with `async_execution=True` under
  `Process.sequential` (deterministic + parallel, per ADR-002), like the other
  chapter tasks.
- **Token accounting (B12):** tokens read from `result.token_usage` and recorded
  by the gatekeeper cost meter into `output/spec_sheet.json`.

### Output contract

The agent writes a Markdown draft to `output/chapters/ch_NN.md`. The
`latex-author` agent transforms it into `tex/sections/ch_bidi.tex`, applying the
`\selectlanguage{hebrew}` block wrapper and verifying every Latin token is inside
a `\foreignlanguage{english}{...}` span. The Hebrew body must contain **no
Arabic** characters (validated in §6).

## 6. QA & Acceptance (B8, B15)

`scripts/qa_pdf.py` runs after the LuaLaTeX → biber → LuaLaTeX → LuaLaTeX build
and asserts the following for the BiDi chapter. All checks are deterministic and
mocked at the unit-test layer (no live LLM/LuaLaTeX I/O in tests, per the rules).

- **Chapter present (B8):** exactly one chapter has Hebrew body text.
- **No missing glyphs (B15):** parse the LuaLaTeX log; fail on "Missing
  character" / `.notdef` warnings for the Hebrew range.
- **No Arabic:** scan `tex/sections/ch_bidi.tex` and the rendered text for the
  Arabic Unicode block; fail if present.
- **Inline English wrapped:** every Latin run in the Hebrew body is inside a
  `\foreignlanguage{english}{...}` span (source-level lint).
- **Links resolve (B15/B9):** any citation in the BiDi chapter resolves and is
  clickable (`hyperref` + biber), no `??` references.
- **Tables fit (B6/B15):** any `tabularx` table in the chapter does not overflow
  `\textwidth` (no "Overfull \hbox" beyond tolerance).

### Acceptance mapping

| Criterion | Requirement | Satisfied by |
|---|---|---|
| B8 | One Hebrew-English BiDi chapter | `ch_bidi.tex` + `bidi_writer` agent (§3, §5) |
| B10 | Real CrewAI multi-agent team | Dedicated `bidi_writer` Agent (§5) |
| B12 | Provider-agnostic config + tokens | `providers.json`, `result.token_usage` (§5) |
| B13 | CrewAI Skills | `skills=["./skills/technical-writer"]` (§5) |
| B6 | Non-overflow table | `layout=tabular` + `tabularx` fit check (§3.1, §6) |
| B15 | BiDi correct | `\foreignlanguage`/`\rlm`/font fallback + QA gate (§3, §4, §6) |

## 7. Definition of Done

- `tex/sections/ch_bidi.tex` compiles cleanly inside `tex/main.pdf` with the
  babel `bidi=basic` stack and no missing-glyph warnings.
- The chapter renders RTL Hebrew body with correctly-directioned inline English
  terms, mirrored punctuation, and no end-of-line drift.
- `bidi_writer` is a distinct CrewAI Agent with the `technical-writer` skill,
  driven by the provider-agnostic config, contributing to the Spec Sheet.
- `scripts/qa_pdf.py` passes all §6 checks; coverage ≥ 85%; ruff zero.
- No Arabic anywhere; exactly one BiDi chapter.
