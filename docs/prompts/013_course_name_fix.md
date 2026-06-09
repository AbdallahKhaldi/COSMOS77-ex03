# Prompt log 013 — Course-name correction (post-Phase-12)

**Authors:** Abdallah Khaldi, Tasneem Natour
**Date:** 2026-06-09

## Trigger

After the v1.00 tag, the partner questioned the title-page course string
`UOH-RL07 — Vibe Coding & AI Agents`. A three-source check (Dr. Segal's own PDFs +
two web sweeps) found that string only inside our own files — it had been copied
verbatim from the build playbook, not from any authoritative source.

## Authoritative source: the syllabus

The official course **syllabus** (`סילבוס 2026 סמסטר א.pdf`, lecturer
**Dr. Yoram Reuven Segal, rmisegal@gmail.com** — matching the collaborator email)
states:

- **Course code:** `203.3763`
- **Course name:** **Orchestration of AI Agents** (אורקסטרציה של סוכני AI)
- **Year:** 2025–2026 · elective · 3 credits
- **"VIBE CODING"** appears only as a *learning outcome* ("ability to manage and
  develop AI agents using VIBE CODING") — a method taught in the course, **not**
  the course title. `UOH-RL07` was only the submission-template filename
  (`uoh-rl07-ex01.docx`), not the course code.

## What was corrected (repo-wide)

Replaced the wrong course name/code everywhere it named the course — the PDF
**title page** (via `config/setup.json`), the **page footer** (`tex/preamble.tex`),
`README.md`, `CLAUDE.md`, `pyproject.toml`, `docs/` (PRD/PLAN/TODO/prompts), and
the package docstrings — with **"Orchestration of AI Agents (203.3763)"**.
Legitimate *method* usages (`vibe-coded`, `vibe-coding`) were deliberately kept,
since the course literally teaches vibe coding. The PDF was recompiled, the cover
+ footer re-eyeballed, gates re-run (98 tests, 97.55%), and the `v1.00` tag/release
re-pointed to the corrected commit.

## Verification

```bash
git grep -n "UOH-RL07"      # (none)
git grep -n "Vibe Coding"   # (none — course-name usage)
grep "Orchestration of AI Agents (203.3763)" tex/main.tex tex/preamble.tex
```
