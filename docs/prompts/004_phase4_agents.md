# Prompt log 004 — Phase 4: CrewAI agents + Skills

**Phase:** 4 — The agent team and the CrewAI Skills (B10, B13)
**Authors:** Abdallah Khaldi, Tasneem Natour
**Date:** 2026-06-09

## Prompt issued

> Phase 4 goal: the agent team and the CrewAI Skills. All TDD; crewai mocked in
> unit tests. Skills (`SKILL.md`, YAML frontmatter + body) for `latex-author`,
> `technical-writer`, `researcher`. `crew/agents.py` — factory functions for
> researcher / planner / chapter_writer (per-chapter) / figure_agent / bidi_writer
> / editor / latex_author (role/goal/backstory/llm/tools/skills, `allow_delegation=False`).
> `crew/tools.py` — web-search tool selection (Serper if keyed, else fallback) +
> FileWriterTool. Wire into `SDK.build_agents()`.

## API verification first (avoided a blind crash)

Before writing builders I introspected the installed **CrewAI 1.14.6** API:
- `Agent` *does* expose a `skills` field — annotated `list[Path | Skill | str]` —
  and **validates the skill path at construction**: a missing dir raises
  `FileNotFoundError`. So skills are wired by **absolute path** to
  `src/cosmos77_ex03/skills/<name>`, CWD-independent.
- SKILL.md needs YAML frontmatter `name` (pattern `^[a-z0-9]+(?:-[a-z0-9]+)*$`) +
  `description`; the loader reads `SKILL.md` from the dir.
- `CodeInterpreterTool` is removed (confirmed). `SerperDevTool`,
  `ScrapeWebsiteTool`, `FileWriterTool` all present.

## What was done

- **3 Skills** copied/adapted from the prebuilt set into
  `src/cosmos77_ex03/skills/{researcher,technical-writer,latex-author}/SKILL.md`
  (distinct `description` selectors). Verified a real `Agent` loads each from disk.
- **`crew/tools.py`** — `web_search_tools()` (Serper if `SERPER_API_KEY`, else a
  keyless `ScrapeWebsiteTool`; `WebsiteSearchTool` deliberately omitted to avoid a
  RAG-embedding dependency on the free tier) + `file_writer_tools()`.
- **`crew/agents.py`** — `make_agent` base + 7 builders (researcher, planner,
  chapter_writer factory, figure_agent, bidi_writer, editor, latex_author);
  `allow_delegation=False`; skills wired per role; latex_author also gets
  FileWriterTool. `build_agents(cfg)` returns the singleton roster.
- **`SDK.build_agents()`** delegates to `crew.agents.build_agents(self.config)`.

## Verification

```bash
uv run python scripts/check_line_cap.py   # agents.py = 144 lines (<=150)
uv run ruff check .                        # zero
uv run pytest -m "not live"                # 64 passed, coverage 100%
```

Unit tests mock `crewai.Agent` + `crewai_tools.*`; no live call in the suite (rule 6).
