# CLAUDE.md — Project rules of engagement (binding for every prompt)

HW3 (CrewAI + LaTeX article generator) for Dr. Yoram Segal's UOH-RL07 course.
Every prompt inherits these rules. HW3 acceptance criteria (B1–B15) are in
../CLAUDE_CODE_PLAYBOOK.md §1.5 — also binding. The PDF is the heart of the grade.

## The 17 rules
1. 150-line hard cap per .py file. Split it.
2. SDK architecture: all business logic via class SDK in src/cosmos77_ex03/sdk/sdk.py.
3. OOP, no duplication. 2 files -> shared module; 3 -> base class/mixin.
4. Zero hardcoded config (topic, language, model, provider, paths) -> config/*.json or .env.
5. uv only. Never pip / venv / python script.py.
6. TDD red->green->refactor. Mock ALL LLM/network/subprocess I/O (CrewAI kickoff, Gemini,
   lualatex). No live calls in the test suite.
7. Coverage >= 85%.
8. ruff check returns zero violations.
9. No secrets in repo. .env.example only; .env (GEMINI_API_KEY) is gitignored.
10. Versioning starts at 1.00 (version.py, every config, git tag v1.00).
11. Conventional Commits per task; reference TODO IDs.
12. Prompt log: every session -> docs/prompts/NNN_*.md.
13. Gatekeeper/cost meter: every LLM call routes through shared/gatekeeper.py; records
    token usage for the Spec Sheet. No hard cap (free tier), but always measured.
14. CLI only (Claude Code terminal). The deliverable is a Python CrewAI program that
    GENERATES the article — never a hand-written or pasted article.
15. Docstrings on every public class/function/module (why, not what).
16. Type hints on every public signature. No bare Any.
17. Deterministic tests. Seed random. Mock I/O. No flakes.

## Language
All code/docs/comments in English. The article is English-primary with one Hebrew–English
BiDi chapter. Arabic is forbidden anywhere in the deliverable.

## When in doubt
Less code, fewer deps, clearer docstrings. Impossible rule for a module -> ADR in
docs/PLAN.md, never a silent violation. The compiled PDF passing the §13.1 checklist
outranks everything else.
