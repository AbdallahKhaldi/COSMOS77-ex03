# Prompt log 003 — Phase 3: Gemini live smoke test

**Phase:** 3 — Prove the free Gemini backend end-to-end
**Authors:** Abdallah Khaldi, Tasneem Natour
**Date:** 2026-06-09

## Prompt issued

> Phase 3 goal: prove the free Gemini backend works end-to-end with a trivial
> one-agent CrewAI run, and that token usage is captured. This phase makes a REAL
> (tiny) Gemini call — unit tests still mock everything. Deliver `crew/smoke.py`
> (one-agent, one-task crew answering "pipeline-ok" via `build_llm(cfg)`,
> returning result + `result.token_usage`), `SDK.smoke()` (records usage via the
> gatekeeper), the `cosmos77-article smoke` CLI subcommand, and mocked tests.

## What was done

- **`crew/smoke.py`** — `build_smoke_crew(cfg)` builds a single `Agent` + `Task`
  (`Process.sequential`) that must reply `pipeline-ok`, using `build_llm(cfg)`;
  `run_smoke(cfg)` runs `kickoff()` and returns `(reply_text, token_usage)`.
- **`SDK.smoke()`** — runs the crew, records `token_usage` through the gatekeeper,
  returns the reply text.
- **CLI** — `cosmos77-article smoke` runs it and prints the reply + the Spec-Sheet
  token line.
- **Tests** — `crewai.Agent/Task/Crew` + `build_smoke_crew` mocked; the SDK test
  patches `crew.smoke.run_smoke`. No live call in the suite (rule 6). 55 tests, 100% cov.

## Real-world finding (why the smoke test matters)

The first live call failed with `ImportError: Google Gen AI native provider not
available`. **CrewAI 1.x routes `gemini/*` through its native Google GenAI
provider, which requires the `google-genai` package** — the playbook's
`google-generativeai` is the legacy SDK. Fixed by `uv add "crewai[google-genai]"`
(adds `google-genai==1.65.0`). This is precisely the integration gap a one-agent
smoke test is designed to surface before the 12-chapter run.

## Verification (live — free Gemini)

```bash
uv run cosmos77-article smoke
# reply: pipeline-ok
# token_usage: {'prompt_tokens': 90, 'completion_tokens': 58, 'total_tokens': 148,
#               'successful_requests': 1, 'provider': 'gemini', 'estimated_cost_usd': 0.0}
```

End-to-end green; cost $0 on the free tier; usage captured for the Spec Sheet (B12).
