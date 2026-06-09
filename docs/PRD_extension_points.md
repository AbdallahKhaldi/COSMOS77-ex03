# PRD — Extension Points (HW1 extensibility fix)

## 1. Purpose & Context

HW1 hardcoded its model id, its agent roster, and its single output language directly in
the Python sources. Adding a provider meant editing the SDK; adding a chapter meant
copy-pasting an `Agent` block; there was no skill abstraction and no second language. This
violated the "zero hardcoded config" rule and made the system brittle.

This PRD defines the **four supported extension points** of `cosmos77_ex03` and proves each
can be exercised **without editing core code** — only JSON config, a new `SKILL.md`, or a
one-line babel font declaration. It is the formal closure of the HW1 extensibility weakness
and the operational contract behind two ADRs:

- **ADR-005 — Provider-agnostic config.** The active LLM is data, never code
  (`config/providers.json`); the factory resolves it at runtime.
- **ADR-006 — SDK single entry.** `src/cosmos77_ex03/sdk/sdk.py` is the only public entry
  point; every extension is reachable through it without subclassing internals.

"Core code" means anything under `src/cosmos77_ex03/{sdk,providers,crew,latex,cli}` that is
not a config loader. Success test: each change below is a **diff touching only
`config/*.json`, `skills/**`, or `tex/preamble.tex`** — zero diffs to `*.py` core modules.

## 2. Design Principles

- **Config over code.** Behaviour is driven by `config/setup.json` and
  `config/providers.json`; loaders in `src/cosmos77_ex03/shared/` parse them.
- **Registry + factory.** A registry maps a string key to a constructor; the factory reads
  the active key and instantiates. New variants register a default, never a caller branch.
- **Loop, don't unroll.** The crew builder iterates a count/list from config, so adding an
  agent is a config number, not a code block.
- **Declarative skills.** Capabilities are Markdown (`SKILL.md` + YAML frontmatter), wired
  by relative path, never imported.

## 3. Extension Points Overview

| # | Extension | File(s) you edit | Core `.py` touched? | Mechanism | Acceptance tie-in |
|---|-----------|------------------|---------------------|-----------|-------------------|
| 1 | Add an LLM provider | `config/providers.json` (+ optional registry default) | No | ADR-005 factory | B12 |
| 2 | Add a chapter / agent | `config/setup.json` (`crew.num_chapters`) | No | writer loop | B1, B3, B10 |
| 3 | Add a CrewAI Skill | `src/cosmos77_ex03/skills/<name>/SKILL.md` + agent `skills=[...]` config | No | declarative selector | B13 |
| 4 | Add an output language | `config/setup.json` (`language`) + one `\babelfont` line | No | babel/fontspec | B8 |

---

## 4. Extension Point 1 — Add an LLM Provider (B12, ADR-005)

### Contract

`config/providers.json` holds an `active` key plus a `providers` map. Each entry declares
`model` and `api_key_env` (the **name** of the env var, never the secret). The SDK calls
`build_llm()` in `src/cosmos77_ex03/providers/factory.py`, which reads `active`, looks up
the block, resolves the key from the environment, and returns a configured CrewAI `LLM`.
The model id is **never** hardcoded — it always comes from the resolved block.

### Before (HW1 — hardcoded, forbidden)

```python
# src/.../crew/build.py  (HW1)
llm = LLM(model="gemini/gemini-2.5-flash", api_key=os.environ["GOOGLE_API_KEY"])
```

### After — config only

```jsonc
// config/providers.json
{
  "active": "groq",                                  // <-- flip provider here
  "providers": {
    "gemini": { "model": "gemini/gemini-2.5-flash", "api_key_env": "GEMINI_API_KEY" },
    "groq":   { "model": "groq/llama-3.3-70b-versatile", "api_key_env": "GROQ_API_KEY" },
    "openai": { "model": "openai/gpt-4o-mini",      "api_key_env": "OPENAI_API_KEY" }
  }
}
```

To add a brand-new provider, append a fourth block (e.g. `"mistral": { "model":
"mistral/mistral-large-latest", "api_key_env": "MISTRAL_API_KEY" }`), set `active` to
`"mistral"`, and put `MISTRAL_API_KEY=...` in the gitignored `.env`. No Python changes.

### When a registry default *is* needed

If a provider needs a non-default keyword (e.g. a custom `base_url`), add a one-line
default to the registry rather than branching in the factory:

```python
# src/.../providers/registry.py
PROVIDER_DEFAULTS["mistral"] = {"base_url": "https://api.mistral.ai/v1"}
```

`build_llm()` merges `PROVIDER_DEFAULTS.get(active, {})` over the config block — so even
this case is an additive registry entry, not a change to the factory's control flow.

### Validation

- Unit test asserts `build_llm()` returns an `LLM` whose `model` equals the active block's
  `model` (the network call is **mocked** — no live Gemini/Groq traffic).
- A test parametrized over all `providers` keys proves each resolves without `KeyError`.

---

## 5. Extension Point 2 — Add a Chapter / Agent (B1, B3, B10)

### Contract

The number of parallel chapter-writers is data: `crew.num_chapters` in
`config/setup.json`. `src/cosmos77_ex03/crew/builder.py` runs a **writer loop**, creating
one CrewAI `Agent` (role `chapter-writer-NN`) and one async `Task` per chapter, then
appends them to the crew. `Process.sequential` with `async_execution=True` on the chapter
tasks gives deterministic-yet-parallel execution (ADR-002) — adding a chapter scales the
loop, it does not add a hierarchical manager.

### Before (HW1 — unrolled, copy-paste)

```python
writer_1 = Agent(role="chapter-writer-1", ...)
writer_2 = Agent(role="chapter-writer-2", ...)
writer_3 = Agent(role="chapter-writer-3", ...)   # add a 4th by copy-paste
```

### After — config bump only

```jsonc
// config/setup.json
{ "crew": { "num_chapters": 7 } }   // was 6 — one extra writer + ch_07.md, no code edit
```

The loop already covers it:

```python
# src/.../crew/builder.py  (core — unchanged when scaling)
writers, tasks = [], []
for n in range(1, cfg.crew.num_chapters + 1):
    agent = self._make_writer(n)                       # allow_delegation=False
    writers.append(agent)
    tasks.append(self._make_chapter_task(agent, n, async_execution=True))
```

Output files `output/chapters/ch_NN.md` and `tex/sections/ch_NN.tex` are named from `n`, so
the new chapter flows into the page count (B1), TOC and running headers (B3), and the
multi-agent crew (B10) automatically. A **specialised** agent (figure/data agent, Hebrew
BiDi writer, editor, latex-author) is added by listing it under `crew.extra_agents` in
config; the builder appends configured roles after the writer loop.

### Validation

- Test sets `num_chapters=2` and asserts the built crew exposes exactly 2 writer agents and
  2 async chapter tasks (CrewAI construction **mocked**; assertions on the builder's
  collected lists — deterministic).

---

## 6. Extension Point 3 — Add a CrewAI Skill (B13)

### Contract

Skills are declarative. Each lives at
`src/cosmos77_ex03/skills/<name>/SKILL.md` with **YAML frontmatter** (`name` +
`description`, the selector CrewAI uses) and a Markdown body of instructions. An agent
gains a skill by listing the relative path in its `skills` array — wired via config, not
imported. Existing skills: `latex-author`, `technical-writer`, `researcher`.

### Before / After

Create the file:

```markdown
<!-- src/cosmos77_ex03/skills/diagram-author/SKILL.md -->
---
name: diagram-author
description: Produces TikZ diagrams and matplotlib graphs for LaTeX figures.
---
# Diagram Author
When asked for a figure, emit compilable TikZ for diagrams (B4) and a matplotlib
script rendering to PDF for data graphs (B5). Never inline raster images.
```

Wire it to the figure/data agent in config:

```jsonc
// config/setup.json  (agent skill wiring — before)
{ "agents": { "figure_data": { "skills": ["./skills/technical-writer"] } } }

// after — one array entry added
{ "agents": { "figure_data": { "skills": ["./skills/technical-writer",
                                          "./skills/diagram-author"] } } }
```

The builder passes the array straight into `Agent(..., skills=cfg.agents.<role>.skills)`.
No core `.py` edit; the new capability is selected by CrewAI from the frontmatter
`description`.

### Validation

- Test asserts every path in every agent's `skills` array resolves to an existing
  `SKILL.md`, and that each `SKILL.md` parses to frontmatter containing `name` and
  `description` (filesystem read, deterministic, no LLM).

---

## 7. Extension Point 4 — Add an Output Language (B8)

### Contract

The article is English-primary with **exactly one** Hebrew-English BiDi chapter; Arabic is
forbidden everywhere. Languages are declared in `config/setup.json` under `language`, and
each non-Latin script needs **one** `\babelfont` line in `tex/preamble.tex` (fontspec +
babel `bidi=basic`, `layout=tabular`). hyperref stays LAST with `unicode=true`.

### Before / After

```jsonc
// config/setup.json  (before)
{ "language": { "main": "english", "secondary": ["hebrew"] } }
```

To enable a second secondary script (e.g. Greek for a notation appendix), extend the list
and add one font line — the loader passes `secondary` into the babel `\babelprovide`
options the preamble template iterates:

```jsonc
// config/setup.json  (after)
{ "language": { "main": "english", "secondary": ["hebrew", "greek"] } }
```

```latex
% tex/preamble.tex  — add ONE line next to the existing Hebrew font
\babelfont[hebrew]{rm}{FreeSerif}   % existing (Culmus / Arial Hebrew fallback on macOS)
\babelfont[greek]{rm}{FreeSerif}    % <-- the only new line
```

The Hebrew BiDi chapter (B8) is unaffected; the new script renders right-to-left or
left-to-right per its babel definition. **Guardrail:** a config validator rejects
`"arabic"` anywhere in `language.*`, enforcing the canon's Arabic ban before any compile.

### Validation

- Test feeds `language.secondary = ["arabic"]` and asserts the loader raises a
  `ValueError` (deterministic; no LaTeX run).
- Test asserts each declared secondary language has a matching `\babelfont` directive
  generated for the preamble (string assertion; `lualatex` is **mocked** in tests).

---

## 8. Non-Goals

- No GUI/web layer — CLI only.
- No runtime provider auto-detection beyond reading `active`; switching is an explicit edit.
- No dynamic skill discovery by disk scan; skills are wired by explicit path so the roster
  stays deterministic and reviewable.
- Adding a language does **not** relax the one-BiDi-chapter rule for B8 or the Arabic ban.

## 9. Acceptance Mapping Summary

- **B1 / B3** — chapter extension (point 2) feeds page count, TOC, and headers.
- **B4 / B5** — new skills (point 3) drive TikZ and matplotlib figures.
- **B8** — language extension (point 4) preserves and parameterises the BiDi chapter.
- **B10** — writer loop keeps the crew genuinely multi-agent at any chapter count.
- **B12** — provider config (point 1) backs the Spec Sheet's provider-agnostic claim.
- **B13** — declarative `SKILL.md` files are the CrewAI Skills deliverable.

Every extension above is exercised by a **mocked, deterministic** unit test, keeping the
suite green at >=85% coverage with zero live LLM/CrewAI/lualatex I/O, per the 17 rules.
