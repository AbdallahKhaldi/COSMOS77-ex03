# Prompt log 012 — Phase 12: Cover PDF + tag + release + Moodle

**Phase:** 12 — Generate the submission cover, tag v1.00, prep submission
**Authors:** Abdallah Khaldi, Tasneem Natour
**Date:** 2026-06-09

## Prompt issued

> Phase 12 goal: generate `COSMOS77-ex03.pdf` from the lecturer's template
> (exercise number = 3, self-score 85, ex03 repo URL), tag, push, prep
> submission. Reuse `scripts/generate_cover_pdf.py`; test asserts exercise = "3"
> and the ex03 URL. Confirm `*.pdf` gitignored (except `tex/main.pdf`). Tag
> `v1.00`, `gh release create`. Print the final summary + the two manual steps.

## What was done

- **Cover field values** (exact, from `build_field_values`): exercise number `3`,
  group `COSMOS77`, self-score `85`, GitHub
  `https://github.com/AbdallahKhaldi/COSMOS77-ex03`, late submission `no`,
  Student 1 `212389712 / Abdallah / Khaldi / עבדאללה / חאלדי`, Student 2
  `323118794 / Tasneem / Natour / תסנים / נאטור`. The template labels were
  verified to match the fill logic; the lecturer's layout is untouched (we only
  append values to existing label paragraphs).
- **Test** (`tests/unit/test_scripts/test_cover.py`): asserts the exercise number
  is `"3"`, the repo URL contains `COSMOS77-ex03`, the self-score is `85`, and
  both partners' IDs are present.
- **Cover PDF** generated to `~/COSMOS77/HW3/COSMOS77-ex03.pdf` (outside the repo;
  `*.pdf` is gitignored except `tex/main.pdf`). Only the script + test are committed.
- **Release:** `git tag -a v1.00`, pushed; `gh release create v1.00`.

## Verification

```bash
uvx --with python-docx --with docx2pdf python scripts/generate_cover_pdf.py \
  --template ~/COSMOS77/HW3/cover_template/uoh-rl07-ex01.docx \
  --output ~/COSMOS77/HW3/COSMOS77-ex03.pdf --self-score 85 --exercise-number 3
# open ~/COSMOS77/HW3/COSMOS77-ex03.pdf  → exercise=3, ex03 URL, layout intact
```

## The two manual steps (only the humans can do these)

1. **Visibility:** the repo is **public**, so the grader (`rmisegal@gmail.com`)
   can read it — no collaborator step needed. (If it were private, add the
   lecturer at `/settings/access`.)
2. **Moodle:** Abdallah **and** Tasneem each upload `~/COSMOS77/HW3/COSMOS77-ex03.pdf`
   to their own Moodle account (the timer is per-student).
