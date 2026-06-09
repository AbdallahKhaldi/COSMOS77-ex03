# PRD — Spec Sheet: tokens / latency / cost / memory (B12)

## 1. Purpose

The Spec Sheet is the project's self-measurement instrument and the observable
proof of acceptance criterion **B12** (provider-agnostic config **plus** a Spec
Sheet reporting tokens, latency, cost, and memory). It is owned by the
**gatekeeper** — the single chokepoint through which every LLM interaction is
accounted (17 Rules, rule 13). After a CrewAI run the gatekeeper accumulates
real usage from `result.token_usage`, times each agent/phase, estimates cost
from a config-driven rate, samples peak memory, and serializes everything to
`output/spec_sheet.json` and a README table. Critically, it does not merely
*report* numbers — it **interprets** them via a mandatory `findings` block
(§8), closing HW1's "numbers aren't analysis" weakness.

## 2. Scope

In scope: `src/cosmos77_ex03/shared/gatekeeper.py` — the `Gatekeeper` class
(`record(...)`, `estimate_cost(...)`, `spec_sheet(...)` plus the interpretation
helpers for the `findings` block); the `output/spec_sheet.json` schema and the
README Spec Sheet table; the per-provider `$/1M` rate contract in
`config/providers.json`; timing/memory sampling; and the `SDK.spec_sheet()`
entry point.

Out of scope (referenced, owned elsewhere): building the `crewai.LLM` and
provider swap — `providers/factory.py` (`PRD_llm_provider.md`); crew/agent
assembly and `kickoff()` — `src/cosmos77_ex03/crew/`; LaTeX compilation and the
article body — B1–B9, B11, B15.

## 3. Data sources

| Metric           | Source                                                        | API / mechanism                                  |
| ---------------- | ------------------------------------------------------------- | ------------------------------------------------ |
| Tokens           | CrewAI `result.token_usage` (`UsageMetrics`)                  | `prompt_tokens`, `completion_tokens`, `total_tokens`, `successful_requests`, `cached_prompt_tokens` |
| Latency          | Wall-clock around each agent task / phase                     | `time.perf_counter()` deltas inside `record(...)`|
| Cost (USD)       | Tokens x per-provider rate                                    | `estimate_cost(...)` reading `config/providers.json` rates |
| Peak memory (MB) | RSS high-water during the run                                 | `tracemalloc.get_traced_memory()` + `resource.getrusage(RUSAGE_SELF).ru_maxrss` |
| Provider / model | Active backend                                                | tagged by `factory.build_llm`, passed to gatekeeper |

CrewAI 1.x exposes usage on the kickoff result (`crew_output.token_usage`) and,
aggregated, via `crew.usage_metrics`; the gatekeeper reads the kickoff result
for exact per-run attribution. `successful_requests` is a sanity check that
agents actually called the model (guards against mock leakage).

## 4. Public interface — `Gatekeeper`

The class lives in `src/cosmos77_ex03/shared/gatekeeper.py`, stays under the
150-line cap (split timing/cost helpers into `_cost.py` / `_timing.py` siblings
if it grows), and carries docstrings + type hints on every public signature
(rules 1, 15, 16). No `Any` in the public surface.

```python
class Gatekeeper:
    """Accounts every LLM interaction and assembles the B12 Spec Sheet.

    Single chokepoint (rule 13): tokens, latency, cost, and memory are recorded
    here so the Spec Sheet is provider-aware and the numbers are interpreted,
    not merely tabulated.
    """

    def record(self, phase: str, agent: str,
               usage: UsageMetrics, seconds: float) -> None:
        """Fold one agent/phase's token usage and wall-clock into the ledger."""

    def estimate_cost(self, usage: UsageMetrics, provider: str) -> float:
        """Return USD cost from per-provider input/output rates in config."""

    def spec_sheet(self) -> SpecSheet:
        """Assemble totals, per-phase breakdown, peak memory, and findings."""
```

`UsageMetrics` and `SpecSheet` are typed value objects (dataclass / `TypedDict`)
in `src/cosmos77_ex03/shared/`. `record(...)` is called once per chapter-writer
task and once per non-writer phase (research, outline, figures, BiDi, edit,
latex-author), so the ledger keys map 1:1 onto the **B10** crew roster.

## 5. Cost model (config-driven, never hardcoded)

Rates live in `config/providers.json` beside each provider (rule 4, B12), so
cost is recomputed for whatever backend is active without touching Python:

```json
{
  "active": "gemini",
  "providers": {
    "gemini": {
      "model": "gemini/gemini-2.5-flash",
      "api_key_env": "GEMINI_API_KEY",
      "rate_usd_per_mtok": { "input": 0.0, "output": 0.0 }
    },
    "groq":   { "rate_usd_per_mtok": { "input": 0.59, "output": 0.79 } },
    "openai": { "rate_usd_per_mtok": { "input": 2.50, "output": 10.00 } }
  }
}
```

`estimate_cost` computes
`(prompt_tokens/1e6 * input) + (completion_tokens/1e6 * output)`. For the active
Gemini free tier the rate is `0.0`, so measured cost is `$0.00` — but the
**machinery is real**: flipping `active` to `openai` immediately yields a
non-zero, correctly attributed cost with zero code change, making the B12
"estimated cost ... computed from a config rate" requirement literal.

## 6. `output/spec_sheet.json` schema

```json
{
  "version": "1.00",
  "provider": "gemini",
  "model": "gemini/gemini-2.5-flash",
  "generated_at": "2026-06-09T13:48:00Z",
  "totals": { "prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0,
              "successful_requests": 0, "wall_clock_seconds": 0.0,
              "estimated_cost_usd": 0.0, "peak_memory_mb": 0.0 },
  "by_phase": [
    { "phase": "research", "agent": "researcher", "total_tokens": 0,
      "seconds": 0.0, "cost_usd": 0.0 }
  ],
  "findings": {
    "most_expensive_phase": "writing", "most_expensive_agent": "chapter-writers",
    "token_share_pct": { "research": 0.0, "writing": 0.0 },
    "scaling_15_to_30_pages": { "tokens_x": 2.0, "cost_usd": 0.0 },
    "notes": "Writing dominates token volume; cost scales ~linearly with page count."
  }
}
```

`by_phase` preserves insertion order so the table mirrors the sequential crew;
`findings` is mandatory and is what closes the HW1 gap (§8).

## 7. README Spec Sheet table (B12, B14)

`SDK.spec_sheet()` returns the `SpecSheet`; a renderer emits the same data as a
Markdown table injected into `README.md` (satisfying **B14**). Example shape:

| Phase / Agent             | Total tokens | Wall-clock (s) | Est. cost (USD) | Share |
| ------------------------- | -----------: | -------------: | --------------: | ----: |
| research / researcher     |       12,400 |           8.10 |         $0.0000 |   18% |
| outline / outline-planner |        3,200 |           2.40 |         $0.0000 |    5% |
| writing / chapter-writers |       41,900 |          21.70 |         $0.0000 |   61% |
| bidi / hebrew-writer      |        4,800 |           4.90 |         $0.0000 |    7% |
| edit / editor-reviewer    |        2,600 |           2.10 |         $0.0000 |    4% |
| **TOTAL** (all 7 phases)  |   **68,300** |      **44.30** |     **$0.0000** | 100%  |

Numbers are illustrative; the renderer fills them from the real run and
regenerates each run, so README and `spec_sheet.json` never drift.

## 8. Interpretation — closing the HW1 "numbers aren't analysis" gap

The gatekeeper computes, not just stores, the analysis. `spec_sheet()` derives:

- **Most expensive phase/agent**: `argmax` over `by_phase` token totals (and
  over cost when a paid provider is active). Expectation: the parallel
  chapter-writers (`writing`) dominate, since they emit the most prose.
- **Token share**: each phase's percentage of `total_tokens`, exposing where
  budget concentrates.
- **Scaling projection**: a defensible linear model — body-token volume is
  roughly proportional to page count, so a 15 -> 30 page article projects `~2x`
  writing tokens and `~2x` cost; fixed-cost phases (outline, latex-author) are
  flagged near-constant. The `notes` field states the conclusion in one sentence.

This turns the Spec Sheet from a metrics dump into an argument: *what cost the
most, why, and what happens if the article doubles.* That sentence-level
conclusion is the graded deliverable, not the raw counts.

## 9. Latency and memory sampling

- **Latency**: each phase is wrapped in a `time.perf_counter()` span. For the
  `async_execution=True` chapter tasks (ADR-002, sequential+async), per-writer
  spans overlap, so the Spec Sheet reports both summed task-seconds **and** the
  run's wall-clock window to make parallelism visible (not double-counted).
- **Memory**: `tracemalloc` is started at SDK entry; `peak_memory_mb` is the max
  of traced peak and `ru_maxrss` (normalized to MB; macOS reports bytes),
  capturing the high-water mark across research, parallel writing, and LaTeX prep.

## 10. SDK integration

`SDK.spec_sheet()` (in `src/cosmos77_ex03/sdk/sdk.py`, the single SDK entry,
rule 2) returns the assembled `SpecSheet` and triggers serialization to
`output/spec_sheet.json` + the README table. The SDK constructs one
`Gatekeeper`, injects it into the run, and after `crew.kickoff()` calls
`gatekeeper.record(...)` per phase from `result.token_usage` and the captured
spans, then `gatekeeper.spec_sheet()`. Agents never write metrics directly; all
accounting flows one-way into the gatekeeper, preserving OOP no-duplication
(rule 3).

## 11. Testing strategy (TDD, deterministic, fully mocked)

Per rules 6, 7, 17: red-green-refactor, **no live LLM/CrewAI calls**, coverage
>= 85%, deterministic, ruff zero (rule 8). Cases:

- **Accumulation**: two synthetic `UsageMetrics` into `record(...)` sum correctly
  in `totals.total_tokens` and `successful_requests`.
- **Cost free tier / paid swap**: Gemini rates `0.0` give `estimate_cost == 0.0`;
  OpenAI rates give the exact `prompt/1e6*input + completion/1e6*output`.
- **Findings**: a ledger where `writing` is the max yields
  `most_expensive_phase == "writing"` and `token_share_pct` summing to 100; the
  15->30 projection doubles writing tokens and cost.
- **Timing/memory**: monkeypatch `time.perf_counter` to a fixed sequence for an
  exact `wall_clock_seconds`; patch `tracemalloc.get_traced_memory`/`getrusage`
  and assert MB normalization with peak = max of both sources.
- **Serialization**: `output/spec_sheet.json` matches the §6 schema and the
  README table renders the same totals (no drift).

`result.token_usage`, `time`, `tracemalloc`, and `resource` are all mocked,
keeping the suite offline and deterministic.

## 12. Acceptance mapping

| Item                                                            | Criterion |
| --------------------------------------------------------------- | --------- |
| Tokens/latency/cost/memory recorded in `output/spec_sheet.json` | B12       |
| README Spec Sheet table                                         | B12, B14  |
| Provider-agnostic, config-driven cost rates                     | B12       |
| Per-agent attribution maps to the real crew roster              | B10       |
| Interpretation (most-expensive + scaling) — HW1 gap closed      | B12       |

## 13. Non-goals and constraints

- No hardcoded rates, model, provider, or paths — config/`.env` only (rule 4);
  no spend cap (Gemini free tier) but always measured (rule 13).
- No live calls in tests; CLI-only; English-only docs and code.
- `gatekeeper.py` stays under 150 lines (split helpers if exceeded, rule 1);
  versioning starts at 1.00; commits are conventional and reference TODO IDs.
