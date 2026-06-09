# COSMOS77-ex03 — CrewAI + LaTeX Article Generator

UOH-RL07 (Vibe Coding & AI Agents, Dr. Yoram Segal) — Homework 3.

A CrewAI multi-agent team researches, writes, and compiles a ~15-page LaTeX
article: **"AI Agents in Production: Architecture, Orchestration & Governance in
2026."** The compiled PDF (`tex/main.pdf`) is the graded deliverable.

> ⚠️ This is a placeholder. The full lab report — architecture diagrams, the
> Spec Sheet, the §13.1 PDF checklist, screenshots, and the self-assessment —
> lands in Phase 10.

## Prerequisites (system, not pip)

- [`uv`](https://docs.astral.sh/uv/) — the only package manager used here.
- **LuaLaTeX + biber** (TeX Live / MacTeX full) and a Hebrew-capable font — to
  compile the PDF. These are system prerequisites, not pip dependencies.
- A **free** `GEMINI_API_KEY` from https://aistudio.google.com/apikey (no card).

## Quickstart (preview)

```bash
uv sync
cp .env.example .env          # then put your free GEMINI_API_KEY in .env
uv run cosmos77-article --help
```

The full pipeline (`research → write → figures → assemble → build → qa`) and its
CLI subcommands come online phase by phase. See `../CLAUDE_CODE_PLAYBOOK.md` for
the complete 13-phase build order.

## License

MIT © 2026 Abdallah Khaldi and Tasneem Natour. See [LICENSE](LICENSE).
