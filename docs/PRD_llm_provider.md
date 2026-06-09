# PRD — Config-driven LLM Provider Factory (B12)

## 1. Purpose

The provider factory is the single, OOP boundary between the COSMOS77-ex03
CrewAI team and whatever LLM backend powers it. It satisfies acceptance
criterion **B12** (provider-agnostic config + Spec Sheet) by guaranteeing that
the active model, its API key source, and its defaults all live in
`config/providers.json` — never in Python. Swapping Gemini for Groq or OpenAI
must require a config edit and an environment variable, with **zero** code
changes and **zero** redeploy of agent logic.

This document specifies the public interface, configuration contract, error
behavior, token-usage surfacing, and TDD strategy for the two files that own
this concern:

- `src/cosmos77_ex03/providers/factory.py`
- `src/cosmos77_ex03/providers/registry.py`

## 2. Scope

In scope:

- Reading and validating `config/providers.json`.
- Building a single `crewai.LLM` instance for the **active** provider.
- A provider registry mapping `provider -> defaults` (model string + key env).
- Resolving the API key from the provider's `api_key_env` via `os.environ`.
- Raising clear, actionable errors for missing keys and unknown providers.
- Surfacing `result.token_usage` to the Spec Sheet through the gatekeeper.

Out of scope (owned elsewhere, referenced here):

- Crew/agent assembly (`src/cosmos77_ex03/crew/`).
- Spec Sheet serialization to `output/spec_sheet.json` (gatekeeper module).
- LaTeX compilation and the article body (B1–B9, B11, B15).

## 3. Configuration contract — `config/providers.json`

The factory consumes a single JSON document with this shape:

```json
{
  "active": "gemini",
  "providers": {
    "gemini": { "model": "gemini/gemini-2.5-flash", "api_key_env": "GEMINI_API_KEY" },
    "groq":   { "model": "groq/llama-3.3-70b-versatile", "api_key_env": "GROQ_API_KEY" },
    "openai": { "model": "gpt-4o-mini", "api_key_env": "OPENAI_API_KEY" }
  }
}
```

Contract rules:

- `active` MUST name a key present in `providers`.
- Each provider entry MUST carry `model` and `api_key_env`.
- The model string is **never** hardcoded in Python; the default is
  `gemini/gemini-2.5-flash` and lives only in config (and as a registry
  fallback default — see §5).
- The file is the only place a reviewer changes to switch backends. This is the
  observable proof of B12 and is reinforced by **ADR-002** (deterministic,
  config-first design).

| Config key                         | Type   | Required | Example                          |
| ---------------------------------- | ------ | -------- | -------------------------------- |
| `active`                           | string | yes      | `"gemini"`                       |
| `providers.<name>.model`           | string | yes      | `"gemini/gemini-2.5-flash"`      |
| `providers.<name>.api_key_env`     | string | yes      | `"GEMINI_API_KEY"`               |

## 4. Public interface

The module exposes a minimal, typed surface (docstrings + type hints required
by the 17 Rules). All functions live within the 150-line-per-file cap; if
either file approaches the cap it is split (e.g. validation helpers move to a
`_schema.py` sibling).

### 4.1 `factory.build_llm(cfg) -> crewai.LLM`

```python
def build_llm(cfg: ProvidersConfig) -> crewai.LLM:
    """Build a CrewAI LLM for the active provider in `cfg`.

    Resolves the active provider's model and api_key_env, reads the key from
    os.environ, and returns a configured crewai.LLM. Raises ProviderConfigError
    for unknown providers and MissingApiKeyError for absent keys.
    """
```

Behavior:

1. Look up `cfg.active` inside `cfg.providers`; unknown -> `ProviderConfigError`.
2. Merge the provider entry with `registry` defaults (entry wins).
3. Resolve `api_key_env` from `os.environ`; absent/empty -> `MissingApiKeyError`.
4. Construct and return `crewai.LLM(model=<model>, api_key=<key>)` using the
   CrewAI 1.x `LLM` class (LiteLLM-backed, so `gemini/...`, `groq/...`, and
   bare OpenAI model ids all route correctly via the model prefix).

`ProvidersConfig` is a small typed value object (dataclass / `TypedDict`)
loaded from `config/providers.json` by the SDK loader; `build_llm` does **not**
read the file itself, keeping it pure and unit-testable.

### 4.2 `registry` — `provider -> defaults`

```python
DEFAULTS: dict[str, ProviderDefaults] = {
    "gemini": ProviderDefaults(model="gemini/gemini-2.5-flash", api_key_env="GEMINI_API_KEY"),
    "groq":   ProviderDefaults(model="groq/llama-3.3-70b-versatile", api_key_env="GROQ_API_KEY"),
    "openai": ProviderDefaults(model="gpt-4o-mini", api_key_env="OPENAI_API_KEY"),
}

def resolve_defaults(provider: str) -> ProviderDefaults:
    """Return registry defaults for `provider`; raise ProviderConfigError if unknown."""
```

The registry is the authoritative list of supported providers and their safe
defaults. An unknown provider raises `ProviderConfigError` with the set of
known providers in the message. Config entries override registry defaults, so
the registry never overrides explicit config; it only fills gaps.

## 5. Error handling (actionable)

Errors are typed and carry remediation text, so a grader running the CLI sees
exactly what to fix.

| Condition                         | Exception              | Message content                                              |
| --------------------------------- | ---------------------- | ------------------------------------------------------------ |
| `active` not in `providers`       | `ProviderConfigError`  | active name + sorted list of known providers                 |
| provider not in registry          | `ProviderConfigError`  | unknown provider + supported set                             |
| `api_key_env` missing from env    | `MissingApiKeyError`   | the env var name + "export it or add it to .env"             |
| entry missing `model`/`api_key_env` | `ProviderConfigError` | which field is missing for which provider                    |

`MissingApiKeyError` example text:

```
Missing API key: environment variable GEMINI_API_KEY is not set.
Export it (export GEMINI_API_KEY=...) or add it to your gitignored .env file.
```

No secret value is ever echoed — only the variable **name**. `.env` is
gitignored (17 Rules: no secrets in repo).

## 6. Token-usage surfacing for the Spec Sheet (B12)

The factory builds the LLM; the **gatekeeper** records usage. After a crew run,
CrewAI returns a result whose `result.token_usage` (a `UsageMetrics` with
`total_tokens`, `prompt_tokens`, `completion_tokens`, `successful_requests`) is
read by the gatekeeper and folded into the Spec Sheet alongside latency, cost,
and memory. The factory contributes the **active model + provider** so the Spec
Sheet attributes tokens to the correct backend. Flow:

- `build_llm` tags the returned LLM context with `provider`/`model` metadata.
- Crew executes; the kickoff result exposes `result.token_usage`.
- Gatekeeper reads `result.token_usage`, multiplies by per-provider price
  (config-driven), and writes `output/spec_sheet.json`.

This keeps B12's Spec Sheet (tokens/latency/cost/memory) provider-aware without
the factory taking a dependency on the gatekeeper (one-way data flow).

## 7. CrewAI 1.x integration

- The single `crewai.LLM` returned by `build_llm` is passed as the `llm=`
  argument to every Agent in `src/cosmos77_ex03/crew/` (researcher,
  outline-planner, chapter-writers, figure/data agent, Hebrew BiDi writer,
  editor/reviewer, latex-author) — supporting **B10** (real multi-agent team).
- Model routing relies on LiteLLM prefixes baked into the model string
  (`gemini/`, `groq/`), so provider swap is purely the config change.
- The factory is invoked once via the single SDK entry
  (`src/cosmos77_ex03/sdk/sdk.py`); agents never instantiate `crewai.LLM`
  directly, preserving OOP no-duplication.

## 8. Testing strategy (TDD, deterministic, all I/O mocked)

Per the 17 Rules: red-green-refactor, **no live LLM/CrewAI calls**, coverage
>= 85%, ruff zero, deterministic. Tests mock `os.environ` and `crewai.LLM`.

- **Model string per provider**: patch `crewai.LLM`; for each of
  `gemini`/`groq`/`openai`, assert `build_llm` calls
  `crewai.LLM(model=<expected>, ...)` with the exact registry/config model.
- **Default model**: with the canonical config, assert the Gemini path yields
  `gemini/gemini-2.5-flash` (no hardcode leaks).
- **Key resolution**: `monkeypatch.setenv("GEMINI_API_KEY", "sentinel")`;
  assert the sentinel is passed to `crewai.LLM(api_key=...)`.
- **Missing key error**: `monkeypatch.delenv(..., raising=False)`; assert
  `MissingApiKeyError` is raised and the message names the env var.
- **Unknown active / unknown provider**: assert `ProviderConfigError` with the
  supported set in the message.
- **Registry override**: config `model` overrides registry default; assert the
  config value wins.
- **Provider swap**: flip `active` to `groq` in an in-memory config; assert the
  Groq model string with no code change.

Mocks ensure determinism and zero network; `crewai.LLM` is replaced with a
`MagicMock` whose call args are inspected (never constructed for real).

## 9. Acceptance mapping

| Item                                        | Criterion |
| ------------------------------------------- | --------- |
| Provider-agnostic config (`providers.json`) | B12       |
| Token usage feeds Spec Sheet                | B12       |
| Single LLM injected into every Agent        | B10       |
| `tex/` project builds with this LLM-driven content | B11  |
| Article correctness produced downstream     | B15       |

## 10. Non-goals and constraints

- No hardcoded model, key, or provider anywhere in `factory.py`/`registry.py`.
- No live calls in tests; CLI-only operation; English-only code and docs.
- Each file stays under the 150-line cap; split helpers if exceeded.
- Versioning starts at 1.00; commits are conventional and reference TODO IDs.
