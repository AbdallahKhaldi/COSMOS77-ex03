# TODO — COSMOS77-ex03 (HW3: CrewAI + LaTeX Article Generator)

Granular task tracker (≥600 items). Format:
`T-NNNN | phase | area | description | DoD | status`.

Phases map to `../CLAUDE_CODE_PLAYBOOK.md` §19 (P0→P12). Phase 0 items are
`done`; later phases start `todo` and are closed with their commit SHA.

T-0001 | P0 | repo | Initialize git repository at project root with main branch | `git rev-parse --is-inside-work-tree` returns true and `.git/` exists | done
T-0002 | P0 | repo | Pin Python interpreter version for the project | `.python-version` exists and contains 3.11 | done
T-0003 | P0 | repo | Author root .gitignore covering .env, .venv, caches, build artifacts | `.gitignore` lists `.env`, `.venv/`, `__pycache__/`, `output/` and `git check-ignore .env` exits 0 | done
T-0004 | P0 | pyproject | Create pyproject.toml [project] table with name cosmos77-ex03 and version 1.00 | `grep 'version = "1.00"' pyproject.toml` matches and name is cosmos77-ex03 | done
T-0005 | P0 | pyproject | Declare runtime dependencies (crewai, litellm, matplotlib, click) in [project] | dependencies array present and `uv sync` resolves without error | done
T-0006 | P0 | pyproject | Declare dev dependency group (pytest, pytest-cov, pytest-mock, ruff) | `[dependency-groups]` block present and `uv run pytest --version` works | done
T-0007 | P0 | pyproject | Set hatchling build-system and wheel target to src/cosmos77_ex03 | `[build-system]` and `[tool.hatch.build.targets.wheel]` point at the package | done
T-0008 | P0 | pyproject | Register console entry point under [project.scripts] for the CLI | `[project.scripts]` maps a command to cosmos77_ex03.cli.main | done
T-0009 | P0 | uv | Generate the locked dependency manifest with uv | `uv.lock` exists and `uv sync --frozen` succeeds | done
T-0010 | P0 | uv | Create the project virtual environment via uv | `.venv/` exists and `uv run python -c "import cosmos77_ex03"` succeeds | done
T-0011 | P0 | config | Author config/providers.json with active=gemini and per-provider model+api_key_env | file parses as JSON, active is "gemini", gemini.model == "gemini/gemini-2.5-flash" | done
T-0012 | P0 | config | Add groq and openai provider blocks for swappable provider config | providers.json contains groq and openai keys each with model + api_key_env | done
T-0013 | P0 | config | Stamp version 1.00 into providers.json | `grep '"version": "1.00"' config/providers.json` matches | done
T-0014 | P0 | config | Author config/setup.json with article title, author, course, instructor, target_pages | setup.json parses and article.title equals the canonical HW3 title | done
T-0015 | P0 | config | Encode crew settings (process sequential, parallel_writers, num_chapters, max_rpm) in setup.json | setup.json crew.process == "sequential" and crew.parallel_writers == true | done
T-0016 | P0 | config | Declare output/tex/figures paths in setup.json paths block | setup.json paths has output_dir, tex_dir, figures_dir | done
T-0017 | P0 | config | Author config/logging_config.json as a dictConfig schema | logging_config.json parses and contains version, handlers, formatters keys | done
T-0018 | P0 | config | Ensure no API keys or secrets are hardcoded in any config/*.json | `grep -rE '(sk-|AIza|gsk_)' config/` returns no matches | done
T-0019 | P0 | env | Author .env.example documenting GEMINI_API_KEY and optional SERPER_API_KEY placeholders | `.env.example` exists with placeholder-only values, no real keys | done
T-0020 | P0 | env | Confirm real .env is gitignored and untracked | `git check-ignore .env` exits 0 and `git ls-files .env` is empty | done
T-0021 | P0 | scripts | Implement scripts/check_line_cap.py enforcing the 150-line hard cap on .py files | script exits non-zero when any .py exceeds 150 lines, 0 otherwise | done
T-0022 | P0 | scripts | Self-verify check_line_cap.py is itself under the 150-line cap | `wc -l scripts/check_line_cap.py` is <= 150 | done
T-0023 | P0 | scripts | Implement scripts/generate_cover_pdf.py stub for the matplotlib cover page | file exists and imports cleanly under `uv run python -c "import ast,pathlib; ast.parse(pathlib.Path('scripts/generate_cover_pdf.py').read_text())"` | done
T-0024 | P0 | scripts | Author scripts/build_pdf.sh running lualatex -> biber -> lualatex -> lualatex | `bash -n scripts/build_pdf.sh` parses and the four-pass sequence is present | done
T-0025 | P0 | scripts | Mark build_pdf.sh executable | `test -x scripts/build_pdf.sh` succeeds | done
T-0026 | P0 | scripts | Implement scripts/qa_pdf.py stub for post-build PDF property checks | qa_pdf.py exists and parses without syntax error | done
T-0027 | P0 | layout | Create src/cosmos77_ex03 package with __init__.py exposing __version__ | `uv run python -c "import cosmos77_ex03; print(cosmos77_ex03.__version__)"` prints 1.00 | done
T-0028 | P0 | layout | Scaffold sdk, shared, providers, crew, skills, figures, latex, cli subpackages | every subdir under src/cosmos77_ex03 contains an __init__.py | done
T-0029 | P0 | layout | Add src/cosmos77_ex03/constants.py with package-level constants and type hints | constants.py imports cleanly and passes ruff | done
T-0030 | P0 | layout | Create CLI entry module src/cosmos77_ex03/cli/main.py | cli/main.py exists and is importable via `uv run python -c "import cosmos77_ex03.cli.main"` | done
T-0031 | P0 | layout | Create output/, logs/, tex/, tex/figures/ directories with .gitkeep where empty | directories exist and tex/.gitkeep + tex/figures/.gitkeep are tracked | done
T-0032 | P0 | tests | Create tests/ package with __init__.py and unit/ + integration/ subpackages | tests/unit/__init__.py and tests/integration/__init__.py exist | done
T-0033 | P0 | tests | Author tests/conftest.py with shared fixtures and mock scaffolding | conftest.py parses and `uv run pytest --collect-only` discovers it | done
T-0034 | P0 | tests | Add tests/unit/test_constants.py covering the constants module | `uv run pytest tests/unit/test_constants.py` passes | done
T-0035 | P0 | tests | Register a "live" pytest marker so live LLM/LaTeX tests can be excluded | pyproject [tool.pytest.ini_options] declares the live marker and `-m "not live"` runs clean | done
T-0036 | P0 | tests | Configure --strict-markers and coverage addopts in pytest config | addopts includes `--strict-markers --cov=src/cosmos77_ex03` | done
T-0037 | P0 | qa | Set coverage gate fail_under = 85 in [tool.coverage.report] | `grep 'fail_under = 85' pyproject.toml` matches | done
T-0038 | P0 | qa | Verify the bootstrap test suite meets the >=85% coverage gate | `uv run pytest -m "not live" --cov-fail-under=85` exits 0 | done
T-0039 | P0 | qa | Configure [tool.ruff] line-length 100 and target-version py311 | pyproject ruff section sets line-length = 100 and target-version = "py311" | done
T-0040 | P0 | qa | Achieve zero ruff lint findings across the repo | `uv run ruff check .` reports All checks passed | done
T-0041 | P0 | qa | Achieve clean ruff format across the repo | `uv run ruff format --check .` reports no files would be reformatted | done
T-0042 | P0 | ci | Author .github/workflows/ci.yml triggering on push and pull_request | ci.yml parses as YAML and defines a jobs section | done
T-0043 | P0 | ci | CI step installs uv and syncs frozen dependencies | ci.yml uses astral-sh/setup-uv and runs `uv sync --frozen` | done
T-0044 | P0 | ci | CI runs ruff check, ruff format --check, and the 150-line cap script | ci.yml contains all three commands as named steps | done
T-0045 | P0 | ci | CI runs pytest excluding live tests with the 85% coverage gate | ci.yml runs `pytest -m "not live" ... --cov-fail-under=85` | done
T-0046 | P0 | ci | CI uploads coverage XML as a build artifact | ci.yml has an actions/upload-artifact step for coverage-xml | done
T-0047 | P0 | precommit | Author .pre-commit-config.yaml with standard hygiene hooks | config includes check-yaml, check-json, end-of-file-fixer, detect-private-key | done
T-0048 | P0 | precommit | Wire ruff and ruff-format pre-commit hooks | .pre-commit-config.yaml includes the astral-sh/ruff-pre-commit repo with ruff + ruff-format ids | done
T-0049 | P0 | precommit | Add a local pre-commit hook invoking the 150-line cap check | a repo:local hook id line-cap-150 runs scripts/check_line_cap.py | done
T-0050 | P0 | docs | Author CLAUDE.md encoding the 17 project rules and design canon | CLAUDE.md exists at repo root and references the 150-line cap, uv-only, and provider-agnostic rules | done
T-0051 | P0 | docs | Author README.md, CHANGELOG.md, CONTRIBUTING.md, and LICENSE at repo root | all four files exist and CHANGELOG records the 1.00 bootstrap entry | done
T-0052 | P1 | docs | Write docs/PRD.md top matter with project id, course UOH-RL07 HW3, lecturer Dr. Yoram Segal, version 1.00, and the exact article title | docs/PRD.md exists and grep finds "AI Agents in Production", "UOH-RL07", "Yoram Segal", and "1.00" | todo
T-0053 | P1 | docs | Add a Goals and Non-Goals section to PRD.md listing the ~15-page PDF as the primary deliverable and excluding any GUI | grep -i "non-goal" docs/PRD.md returns a section and "CLI only" appears, no "GUI" feature listed | todo
T-0054 | P1 | docs | Add a Personas/User-Stories section to PRD.md (student author, reviewer, grader) tied to acceptance IDs | docs/PRD.md contains "As a reviewer" and at least three persona stories each referencing a B-id | todo
T-0055 | P1 | docs | Build the Functional Requirements table in PRD.md mapping FR-01..FR-15 to acceptance criteria B1..B15 | grep -c "FR-" docs/PRD.md >= 15 and each B1..B15 token is present | todo
T-0056 | P1 | docs | Add Non-Functional Requirements to PRD.md (coverage>=85%, 150-line cap, ruff zero, deterministic mocked tests, uv-only) | grep finds "85%", "150", "ruff", and "uv" within an NFR section of docs/PRD.md | todo
T-0057 | P1 | docs | Add a Constraints/Standards section to PRD.md enumerating all 17 project rules as a checklist | docs/PRD.md lists 17 numbered constraint items and includes "single SDK entry" and "no hardcoded config" | todo
T-0058 | P1 | docs | Document the language policy in PRD.md (English-primary, exactly one Hebrew-English BiDi chapter, Arabic forbidden) | grep -i "Arabic forbidden" docs/PRD.md and "exactly one" BiDi chapter statement both present | todo
T-0059 | P1 | docs | Add an Acceptance Criteria section to PRD.md restating B1..B15 verbatim with their verifiable checks | docs/PRD.md contains all of B1 through B15 as distinct bullet lines | todo
T-0060 | P1 | docs | Add a Deliverables/Artifacts table to PRD.md listing output/ files and tex/main.pdf as the graded heart | grep finds "tex/main.pdf", "output/spec_sheet.json", and "output/outline.json" in docs/PRD.md | todo
T-0061 | P1 | docs | Add a Glossary to PRD.md defining Crew, Agent, Task, Skill, Spec Sheet, gatekeeper cost meter, BiDi | docs/PRD.md has a "Glossary" heading with >=7 defined terms | todo
T-0062 | P1 | docs | Verify docs/PRD_llm_provider.md specifies provider-agnostic config (active provider + per-provider model + api_key_env) with no hardcoded model | grep -i "providers.json" and "api_key_env" present and grep -i "gemini-2.5-flash" appears only as example default | todo
T-0063 | P1 | docs | Document the swappable-provider mechanism (Gemini default, Groq/OpenAI alternates) in PRD_llm_provider.md with the SDK seam | docs/PRD_llm_provider.md names all three providers and references "sdk/sdk.py" as the single entry | todo
T-0064 | P1 | docs | Verify docs/PRD_research_tool.md describes reference/Agent_Architecture_2026.pdf as primary local source and the research.md output | grep finds "Agent_Architecture_2026.pdf" and "output/research.md" in docs/PRD_research_tool.md | todo
T-0065 | P1 | docs | Verify docs/PRD_crew_design.md enumerates all agents (researcher, outline-planner, chapter-writers, figure/data, BiDi writer, editor, latex-author) | grep -c "Agent" docs/PRD_crew_design.md >= 7 and each agent role name appears | todo
T-0066 | P1 | docs | Document Process.sequential with async_execution=True chapter tasks (not hierarchical) and the no-delegation default in PRD_crew_design.md | grep finds "Process.sequential", "async_execution", and "allow_delegation" in docs/PRD_crew_design.md | todo
T-0067 | P1 | docs | Record that CodeInterpreterTool is removed and tokens come from result.token_usage in PRD_crew_design.md | grep -i "CodeInterpreterTool" notes its removal and "result.token_usage" is referenced | todo
T-0068 | P1 | docs | Verify docs/PRD_skills.md defines SKILL.md format (YAML frontmatter name+description selector + Markdown body) for latex-author, technical-writer, researcher | docs/PRD_skills.md lists all three skill names and shows the frontmatter schema | todo
T-0069 | P1 | docs | Document skill wiring per agent via skills=["./skills/<name>"] in PRD_skills.md | grep finds the skills=[...] wiring pattern in docs/PRD_skills.md | todo
T-0070 | P1 | docs | Verify docs/PRD_latex_template.md specifies the LuaLaTeX + babel(bidi=basic,layout=tabular) + fontspec/\babelfont stack | grep finds "LuaLaTeX", "bidi=basic", and "\babelfont" in docs/PRD_latex_template.md | todo
T-0071 | P1 | docs | Document the package set and ordering in PRD_latex_template.md (amsmath, booktabs+tabularx, graphicx, tikz, fancyhdr, biblatex+biber, hyperref LAST) | docs/PRD_latex_template.md states hyperref loads last with unicode=true and lists all packages | todo
T-0072 | P1 | docs | Document the compile sequence lualatex -> biber -> lualatex -> lualatex in PRD_latex_template.md | grep finds the four-step compile order in docs/PRD_latex_template.md | todo
T-0073 | P1 | docs | Verify docs/PRD_figure_generation.md covers the matplotlib->PDF graph (B5) and the TikZ diagram (B4) mechanisms | grep finds "matplotlib", "PDF", and "TikZ" in docs/PRD_figure_generation.md | todo
T-0074 | P1 | docs | Document deterministic figure generation (fixed seed, no live data) in PRD_figure_generation.md | grep -i "seed" or "deterministic" present in docs/PRD_figure_generation.md | todo
T-0075 | P1 | docs | Verify docs/PRD_bidi.md defines the single Hebrew-English BiDi chapter, font fallback (FreeSerif/Culmus, Arial Hebrew on macOS), and Arabic prohibition | grep finds "Culmus", "Arial Hebrew", and "Arabic" prohibition in docs/PRD_bidi.md | todo
T-0076 | P1 | docs | Verify docs/PRD_extension_points.md documents how providers, skills, and chapters are added without code edits to core | grep -i "extension" lists at least three named seams in docs/PRD_extension_points.md | todo
T-0077 | P1 | docs | Create the missing 9th mechanism PRD docs/PRD_spec_sheet.md describing the gatekeeper cost meter (tokens/latency/cost/memory -> output/spec_sheet.json) | docs/PRD_spec_sheet.md exists and grep finds "tokens", "latency", "cost", "memory", and "spec_sheet.json" | todo
T-0078 | P1 | docs | Document the spec_sheet.json schema (per-run fields and aggregate totals) in PRD_spec_sheet.md | docs/PRD_spec_sheet.md contains a JSON schema block listing tokens/latency/cost/memory keys | todo
T-0079 | P1 | docs | Create the missing 10th mechanism PRD docs/PRD_sdk_cli.md describing the single SDK entry sdk/sdk.py and the CLI-only surface | docs/PRD_sdk_cli.md exists and references "sdk/sdk.py" and the "cosmos77-article" CLI command | todo
T-0080 | P1 | docs | Document the prompt-log-per-session mechanism in PRD_sdk_cli.md (where logs land, format) | grep -i "prompt log" docs/PRD_sdk_cli.md and a logs/ path reference present | todo
T-0081 | P1 | docs | Add a cross-reference index at the end of PRD.md linking each of the 10 mechanism PRDs by relative path | docs/PRD.md links all 10 PRD_*.md files and grep -c "PRD_" docs/PRD.md >= 10 | todo
T-0082 | P1 | docs | Verify all 10 mechanism PRD files exist and are non-empty | ls docs/PRD_*.md lists 10 files and none is zero-byte | todo
T-0083 | P1 | docs | Create docs/PLAN.md skeleton with sections C4, Sequence, ADRs, Risks, and Milestones | docs/PLAN.md exists with all five headings present | todo
T-0084 | P1 | docs | Write the C4 Context diagram (level 1) in PLAN.md showing the article generator, the LLM provider, and the local reference PDF | docs/PLAN.md C4 section contains a Context-level diagram (mermaid or ASCII) naming external systems | todo
T-0085 | P1 | docs | Write the C4 Container diagram (level 2) in PLAN.md showing sdk, crew, providers, skills, figures, latex, cli containers | docs/PLAN.md shows containers matching src/cosmos77_ex03 subpackages | todo
T-0086 | P1 | docs | Write the C4 Component diagram (level 3) in PLAN.md decomposing the crew package into its agents and tasks | docs/PLAN.md component diagram names each agent and the task graph | todo
T-0087 | P1 | docs | Add the end-to-end runtime sequence diagram to PLAN.md (CLI -> SDK -> Crew -> agents -> LaTeX build -> spec_sheet) | docs/PLAN.md contains a sequence diagram with lifelines for CLI, SDK, Crew, and the LaTeX build | todo
T-0088 | P1 | docs | Write ADR-001 in PLAN.md recording the provider-agnostic config and Gemini-as-default decision | docs/PLAN.md contains "ADR-001" with Context/Decision/Consequences subsections | todo
T-0089 | P1 | docs | Write ADR-002 in PLAN.md recording sequential+async_execution over hierarchical (delegation ping-pong, determinism, parallelism) | grep finds "ADR-002" and the rationale "sequential" vs "hierarchical" in docs/PLAN.md | todo
T-0090 | P1 | docs | Write ADR-003 in PLAN.md recording the LuaLaTeX + babel bidi=basic choice for BiDi over alternatives | docs/PLAN.md contains "ADR-003" naming LuaLaTeX/babel and rejected alternatives | todo
T-0091 | P1 | docs | Write ADR-004 in PLAN.md recording the single-SDK-entry / mock-all-LLM-IO testing strategy | docs/PLAN.md contains "ADR-004" referencing the SDK seam and mocked deterministic tests | todo
T-0092 | P1 | docs | Write ADR-005 in PLAN.md recording removal of CodeInterpreterTool and reliance on a dedicated figure agent | docs/PLAN.md contains "ADR-005" noting "CodeInterpreterTool" removal | todo
T-0093 | P1 | docs | Add a Risks register to PLAN.md with >=8 risks, each with likelihood, impact, and mitigation | docs/PLAN.md Risks table has >=8 rows and columns for likelihood/impact/mitigation | todo
T-0094 | P1 | docs | Add a risk row for LaTeX BiDi font availability on macOS with the Arial Hebrew fallback mitigation in PLAN.md | grep -i "Culmus" or "Arial Hebrew" appears in the PLAN.md Risks section | todo
T-0095 | P1 | docs | Add a risk row for Gemini free-tier rate limits with the provider-swap mitigation in PLAN.md | grep -i "rate limit" present in PLAN.md Risks section with a swap mitigation | todo
T-0096 | P1 | docs | Add a Milestones/phase timeline to PLAN.md mapping phases P1..Pn to acceptance B-ids | docs/PLAN.md Milestones section maps each phase to one or more B-ids | todo
T-0097 | P1 | docs | Create docs/TODO.md header with versioning note, ID scheme (P<phase>-<area>-NNN), and status legend | docs/TODO.md exists with an ID-scheme description and a legend of statuses including "todo" | todo
T-0098 | P1 | docs | Assemble docs/TODO.md from the _todo_parts/P*.txt fragments so it contains >=600 task lines | wc -l docs/TODO.md >= 600 and every data line ends with a status token | todo
T-0099 | P1 | docs | Group TODO.md lines into per-area sections (config, sdk, providers, crew, skills, figures, latex, qa, tests, docs, ci, cover) | docs/TODO.md has a heading for each of the 12 areas | todo
T-0100 | P1 | docs | Add a traceability appendix to TODO.md mapping each acceptance B1..B15 to the TODO IDs that satisfy it | docs/TODO.md appendix lists B1..B15 each with at least one referenced TODO ID | todo
T-0101 | P1 | docs | Add a documentation completeness check to TODO.md verifying PRD.md, the 10 PRDs, PLAN.md, and README.md all exist | docs/TODO.md contains a self-referential docs-check task and grep confirms all four artifact names | todo
T-0102 | P2 | shared | Create src/cosmos77_ex03/shared/__init__.py exporting the shared package surface | python -c "import cosmos77_ex03.shared" exits 0 | todo
T-0103 | P2 | tests | Add tests/shared/test_version.py asserting version string equals "1.00" and matches a MAJOR.MINOR regex | pytest tests/shared/test_version.py fails red before version.py exists | todo
T-0104 | P2 | shared | Implement src/cosmos77_ex03/shared/version.py exposing __version__ = "1.00" with module docstring and type hint | test_version.py passes green | todo
T-0105 | P2 | shared | Add a get_version() function in version.py returning __version__ as str | test asserts get_version() == "1.00" | todo
T-0106 | P2 | tests | Add tests/shared/test_constants.py asserting required path constants and default keys exist | pytest collects and fails red before constants.py | todo
T-0107 | P2 | shared | Implement src/cosmos77_ex03/shared/constants.py defining CONFIG_DIR, OUTPUT_DIR, TEX_DIR, REFERENCE_DIR as absolute pathlib.Path constants | test_constants.py path assertions pass | todo
T-0108 | P2 | shared | Add filename constants (SETUP_JSON, PROVIDERS_JSON, LOGGING_CONFIG_JSON, SPEC_SHEET_JSON) in constants.py | test asserts constant string values | todo
T-0109 | P2 | shared | Keep constants.py under 150 lines and free of any hardcoded model name or api key | scripts/check_line_cap.py reports constants.py OK and grep finds no model string | todo
T-0110 | P2 | tests | Add tests/shared/test_config_dotpath.py with a fixture JSON for dot-path lookup happy path | test red before config.py loader exists | todo
T-0111 | P2 | config | Implement src/cosmos77_ex03/shared/config.py with load_json(path) returning a parsed dict | test_config loads fixture and asserts dict equality | todo
T-0112 | P2 | config | Add Config.get(dot_path, default=None) resolving nested keys like "providers.active" via split on "." | test asserts nested value returned | todo
T-0113 | P2 | config | Make Config.get return the provided default when any path segment is missing | test_config_dotpath missing-key case returns sentinel default | todo
T-0114 | P2 | config | Raise KeyError in Config.require(dot_path) when key absent and no default semantics apply | test asserts pytest.raises(KeyError) | todo
T-0115 | P2 | config | Cache parsed config files in Config so repeated loads do not re-read disk | test patches builtins.open and asserts it is called once across two get calls | todo
T-0116 | P2 | config | Support env-var override resolution in config.py (value "${ENV:NAME}" expands from os.environ) | test sets monkeypatch.setenv and asserts expanded value | todo
T-0117 | P2 | config | Keep config.py at or under 150 lines, splitting helpers into shared/_config_io.py if needed | check_line_cap.py reports config.py OK | todo
T-0118 | P2 | tests | Add tests/shared/test_config_providers.py loading config/providers.json structure (active, providers map) | test red before providers.json present | todo
T-0119 | P2 | config | Create config/providers.json with active="gemini" and per-provider model + api_key_env entries (gemini/groq/openai) | test asserts active key and gemini.model present, no literal key value | todo
T-0120 | P2 | config | Create config/setup.json holding project metadata (title, author, course, lecturer, date) with no secrets | test_config reads title and lecturer fields | todo
T-0121 | P2 | config | Create config/logging_config.json with handlers, formatters, and root level fields | test asserts json parses and contains "handlers" key | todo
T-0122 | P2 | tests | Add tests/shared/test_logging_setup.py asserting configure_logging returns a configured Logger | test red before logging_setup.py | todo
T-0123 | P2 | logging | Implement src/cosmos77_ex03/shared/logging_setup.py reading logging_config.json via Config and calling dictConfig | test patches logging.config.dictConfig and asserts called with parsed dict | todo
T-0124 | P2 | logging | Add get_logger(name) helper in logging_setup.py returning logging.getLogger(name) | test asserts returned logger.name equals requested name | todo
T-0125 | P2 | logging | Ensure logging_setup writes a per-session prompt-log path under output/ derived from constants | test asserts log handler filename resolves under OUTPUT_DIR | todo
T-0126 | P2 | logging | Keep logging_setup.py under 150 lines | check_line_cap.py reports logging_setup.py OK | todo
T-0127 | P2 | tests | Add tests/shared/test_gatekeeper.py for recording a single token-usage entry | test red before gatekeeper.py | todo
T-0128 | P2 | gatekeeper | Implement src/cosmos77_ex03/shared/gatekeeper.py with CostMeter class storing prompt/completion/total tokens | test instantiates CostMeter and asserts zeroed counters | todo
T-0129 | P2 | gatekeeper | Add CostMeter.record(prompt_tokens, completion_tokens) accumulating totals | test asserts totals after two record calls | todo
T-0130 | P2 | gatekeeper | Add CostMeter.record_usage(token_usage) accepting a CrewAI-style usage object/dict | test passes a fake usage and asserts mapped fields | todo
T-0131 | P2 | gatekeeper | Add latency tracking via CostMeter.start()/stop() using a monotonic clock | test monkeypatches time and asserts elapsed seconds computed | todo
T-0132 | P2 | gatekeeper | Add memory sampling helper recording peak RSS for the Spec Sheet | test patches resource/psutil call and asserts value stored | todo
T-0133 | P2 | gatekeeper | Add CostMeter.cost_estimate(rate_per_1k) computing cost from total tokens | test asserts cost equals tokens/1000*rate | todo
T-0134 | P2 | gatekeeper | Add CostMeter.to_spec_sheet() returning dict with tokens, latency, cost, memory keys | test asserts all four keys present | todo
T-0135 | P2 | gatekeeper | Add write_spec_sheet(meter, path) dumping to output/spec_sheet.json via constants | test patches open and asserts json.dump payload shape | todo
T-0136 | P2 | gatekeeper | Keep gatekeeper.py under 150 lines, extracting spec-sheet IO to gatekeeper_io.py if needed | check_line_cap.py reports gatekeeper modules OK | todo
T-0137 | P2 | tests | Add tests/providers/test_registry.py asserting registered provider names resolve to builder callables | test red before registry.py | todo
T-0138 | P2 | providers | Implement src/cosmos77_ex03/providers/registry.py mapping provider name to a builder via a register decorator | test registers a dummy and asserts lookup returns it | todo
T-0139 | P2 | providers | Add registry.get(name) raising KeyError with available-names message for unknown provider | test asserts KeyError on "nope" | todo
T-0140 | P2 | providers | Register gemini, groq, and openai builder stubs in registry without instantiating live clients | test asserts the three names are present in registry keys | todo
T-0141 | P2 | tests | Add tests/providers/test_factory.py building an LLM from providers.json with the active provider | test red before factory.py | todo
T-0142 | P2 | providers | Implement src/cosmos77_ex03/providers/factory.py make_llm(config) reading active provider then model + api_key_env | test patches the crewai LLM class and asserts model arg comes from config | todo
T-0143 | P2 | providers | Resolve api key from os.environ[api_key_env] in factory and never read a literal key | test monkeypatches env and asserts key passed, missing env raises clear error | todo
T-0144 | P2 | providers | Ensure factory never hardcodes "gemini/gemini-2.5-flash"; model derives only from config | grep -R "gemini-2.5-flash" src/cosmos77_ex03/providers returns nothing | todo
T-0145 | P2 | providers | Add factory.make_llm provider-switch test proving groq/openai selection changes model | test sets active=groq and asserts groq model passed to mocked LLM | todo
T-0146 | P2 | providers | Keep factory.py and registry.py each under 150 lines | check_line_cap.py reports providers modules OK | todo
T-0147 | P2 | sdk | Create src/cosmos77_ex03/sdk/sdk.py as the single SDK entry with a Cosmos77SDK class skeleton | python -c "from cosmos77_ex03.sdk.sdk import Cosmos77SDK" exits 0 | todo
T-0148 | P2 | sdk | Add SDK method stubs (research, plan_outline, write_chapters, build_latex, run) raising NotImplementedError | test asserts each stub raises NotImplementedError | todo
T-0149 | P2 | sdk | Wire SDK __init__ to load Config, configure_logging, and a CostMeter without performing live calls | test constructs SDK with patched deps and asserts attributes set | todo
T-0150 | P2 | tests | Run full suite with coverage and confirm shared+providers+sdk lines exceed 85 percent | pytest --cov reports >=85% and ruff check src tests returns zero findings | todo
T-0151 | P2 | docs | Append P2 module map (version, config, logging_setup, gatekeeper, constants, factory, registry, sdk) to docs/PLAN.md | docs/PLAN.md contains a P2 section listing the eight modules | todo
T-0152 | P3 | config | Add smoke section to config/setup.json with smoke_prompt and smoke_max_tokens keys | config/setup.json parses via json.load and contains key "smoke" with subkeys smoke_prompt, smoke_max_tokens | todo
T-0153 | P3 | config | Document the smoke config schema in config/README or inline comment-free JSON note in docs | docs reference for smoke config exists and lists each key with type | todo
T-0154 | P3 | config | Ensure smoke config reader uses existing shared config loader, no new file IO duplication | grep shows smoke reader calls shared.config.load_setup, not open() directly | todo
T-0155 | P3 | providers | Confirm providers.json active provider resolves to gemini/gemini-2.5-flash for smoke run | test_providers_active_resolves_gemini asserts resolved model string equals config value | todo
T-0156 | P3 | providers | Verify provider api_key_env lookup returns env var name (GEMINI_API_KEY) for smoke path | test_provider_api_key_env_name asserts api_key_env equals "GEMINI_API_KEY" | todo
T-0157 | P3 | providers | Add guard that smoke aborts with clear error if api_key env var is unset | test_smoke_missing_key_raises asserts RuntimeError mentioning GEMINI_API_KEY | todo
T-0158 | P3 | providers | Ensure model id is read from providers.json at call time, never hardcoded in smoke code | grep -r "gemini-2.5-flash" src/cosmos77_ex03 returns no match outside config loaders | todo
T-0159 | P3 | crew | Create src/cosmos77_ex03/crew/smoke.py defining a one-agent single-task crew builder | file crew/smoke.py exists and exports build_smoke_crew callable | todo
T-0160 | P3 | crew | Define the single smoke Agent with role, goal, backstory sourced from config not literals | test_smoke_agent_fields asserts role/goal/backstory are non-empty strings from config | todo
T-0161 | P3 | crew | Set allow_delegation False on the smoke agent per worker default rule | test_smoke_agent_no_delegation asserts agent.allow_delegation is False | todo
T-0162 | P3 | crew | Define one smoke Task with description and expected_output, no async_execution | test_smoke_task_sync asserts task.async_execution is False or unset | todo
T-0163 | P3 | crew | Wire smoke Crew with Process.sequential and the single agent and task | test_smoke_crew_sequential asserts crew.process == Process.sequential | todo
T-0164 | P3 | crew | Inject the provider LLM into the smoke agent from providers config, no inline model | test_smoke_agent_llm_from_config asserts llm model equals resolved provider model | todo
T-0165 | P3 | crew | Keep crew/smoke.py under the 150-line hard cap, splitting helpers if needed | scripts/check_line_cap.py reports crew/smoke.py <= 150 lines | todo
T-0166 | P3 | crew | Expose build_smoke_crew via crew package __init__ for import by SDK | from cosmos77_ex03.crew import build_smoke_crew succeeds in a test | todo
T-0167 | P3 | crew | Return a typed result object/dict from smoke kickoff including output text | test_smoke_kickoff_returns_output asserts result has non-empty output field (mocked) | todo
T-0168 | P3 | crew | Extract token_usage from result.token_usage after kickoff | test_smoke_token_usage_extracted asserts usage prompt/completion/total ints present | todo
T-0169 | P3 | sdk | Add SDK.smoke() method to src/cosmos77_ex03/sdk/sdk.py as single entry point | test_sdk_has_smoke asserts callable(SDK.smoke) | todo
T-0170 | P3 | sdk | SDK.smoke builds the smoke crew via crew.smoke and kicks it off | test_sdk_smoke_calls_build asserts build_smoke_crew invoked once (mock) | todo
T-0171 | P3 | sdk | SDK.smoke returns a SmokeResult with output, tokens, latency_ms fields | test_sdk_smoke_result_shape asserts result has output, tokens, latency_ms attributes | todo
T-0172 | P3 | sdk | SDK.smoke measures wall-clock latency around kickoff using time.perf_counter | test_sdk_smoke_latency_positive asserts latency_ms >= 0 with mocked clock | todo
T-0173 | P3 | sdk | SDK.smoke routes token usage into the gatekeeper cost meter | test_sdk_smoke_records_usage asserts gatekeeper.record called with token counts | todo
T-0174 | P3 | sdk | Keep sdk.py within 150-line cap by delegating smoke logic to a helper module | scripts/check_line_cap.py reports sdk.py <= 150 lines | todo
T-0175 | P3 | sdk | Add docstring and full type hints to SDK.smoke public method | test_sdk_smoke_annotations asserts return annotation present and not empty | todo
T-0176 | P3 | sdk | Ensure SDK.smoke raises a clear error when provider/key invalid before kickoff | test_sdk_smoke_invalid_provider_raises asserts ValueError/RuntimeError raised | todo
T-0177 | P3 | crew | Gatekeeper records usage for the smoke run including model name and provider | test_gatekeeper_smoke_record_model asserts recorded entry includes provider+model | todo
T-0178 | P3 | crew | Gatekeeper accumulates prompt, completion, and total tokens for smoke | test_gatekeeper_accumulates_tokens asserts totals equal sum of recorded values | todo
T-0179 | P3 | crew | Gatekeeper exposes a snapshot method returning current usage for Spec Sheet | test_gatekeeper_snapshot asserts snapshot dict has tokens and call count | todo
T-0180 | P3 | crew | Gatekeeper computes estimated cost from per-token rate in config | test_gatekeeper_cost_estimate asserts cost equals tokens * rate from config | todo
T-0181 | P3 | cli | Add a "smoke" subcommand to the CLI argument parser | test_cli_has_smoke_subcommand asserts "smoke" present in parser subcommands | todo
T-0182 | P3 | cli | CLI smoke subcommand invokes SDK.smoke and prints output and token summary | test_cli_smoke_invokes_sdk asserts SDK.smoke called once (mock) | todo
T-0183 | P3 | cli | CLI smoke prints latency_ms and total tokens to stdout in readable form | test_cli_smoke_stdout asserts captured stdout contains "tokens" and "ms" | todo
T-0184 | P3 | cli | CLI smoke exits 0 on success and non-zero on smoke failure | test_cli_smoke_exit_codes asserts exit 0 on mock success, 1 on raised error | todo
T-0185 | P3 | cli | Keep CLI smoke handler under 150-line cap, separate from arg parsing module | scripts/check_line_cap.py reports cli smoke handler file <= 150 lines | todo
T-0186 | P3 | cli | Add --json flag to smoke subcommand to emit machine-readable result | test_cli_smoke_json asserts stdout parses as JSON with output and tokens keys | todo
T-0187 | P3 | tests | Create conftest fixture that mocks crewai Crew.kickoff returning canned output+usage | fixture mock_kickoff importable and yields object with output and token_usage | todo
T-0188 | P3 | tests | Mock the Gemini/LLM client so no live network call occurs in any smoke test | test suite passes with network disabled (monkeypatched LLM), no real HTTP | todo
T-0189 | P3 | tests | Assert no live CrewAI kickoff happens by patching crewai.Crew in tests | test_no_live_crewai asserts Crew constructor patched and real kickoff never run | todo
T-0190 | P3 | tests | Add unit test for build_smoke_crew structure with crewai fully mocked | test_build_smoke_crew_mocked passes asserting agents and tasks counts equal 1 | todo
T-0191 | P3 | tests | Add deterministic test for token extraction using fixed mocked token_usage | test_token_extraction_deterministic asserts identical result across two runs | todo
T-0192 | P3 | tests | Add test that SDK.smoke propagates gatekeeper snapshot into returned result | test_smoke_result_includes_usage asserts result tokens match gatekeeper snapshot | todo
T-0193 | P3 | tests | Add CLI integration test invoking main(["smoke"]) with all I/O mocked | test_cli_main_smoke passes end-to-end with mocks and exit code 0 | todo
T-0194 | P3 | tests | Ensure all smoke tests are deterministic with seeded/mocked clock and usage | rerunning pytest twice yields identical pass output for smoke tests | todo
T-0195 | P3 | qa | Run ruff over crew/smoke.py, sdk smoke helper, cli smoke handler | ruff check reports zero errors for the smoke-related files | todo
T-0196 | P3 | qa | Verify coverage for smoke modules meets project threshold | coverage report shows smoke modules at or above 85 percent | todo
T-0197 | P3 | qa | Add prompt log entry capturing the smoke session prompt and template | output prompt log file contains a dated smoke session entry | todo
T-0198 | P3 | docs | Document the smoke subcommand usage in README CLI section | README contains "smoke" usage example with uv run invocation | todo
T-0199 | P3 | docs | Add a TODO/PLAN note marking P3 live smoke milestone and its DoD | docs/PLAN.md references P3 smoke milestone with acceptance link to B10/B12 | todo
T-0200 | P3 | ci | Add a live-smoke manual instruction (not in CI) documenting how to run real Gemini call | docs note describes uv run cli smoke with GEMINI_API_KEY set, excluded from pytest | todo
T-0201 | P3 | docs | Record a conventional commit referencing P3 smoke TODO IDs after merge | git log shows commit "feat(smoke): ..." referencing P3 task ids | todo
T-0202 | P4 | crew | Create src/cosmos77_ex03/crew/agents/ package dir with __init__.py exporting the agent factory functions | __init__.py exists and `from cosmos77_ex03.crew.agents import build_researcher_agent` imports without error | todo
T-0203 | P4 | crew | Implement researcher Agent factory in crew/agents/researcher.py reading role/goal/backstory from config not hardcoded | test_researcher_agent_uses_config asserts role/goal pulled from config dict; file <=150 lines | todo
T-0204 | P4 | crew | Wire researcher Agent skills=["./skills/researcher"] and allow_delegation=False in its factory | test_researcher_skills_wired asserts agent.skills contains the researcher skill path and allow_delegation is False | todo
T-0205 | P4 | crew | Implement outline-planner Agent factory in crew/agents/planner.py with allow_delegation=False | test_planner_agent_built asserts role contains "outline"/"plan" and allow_delegation is False | todo
T-0206 | P4 | crew | Implement chapter-writer Agent factory in crew/agents/chapter_writer.py parameterized by chapter id/title | test_chapter_writer_factory_per_chapter asserts distinct agents produced for two chapter ids with titles injected | todo
T-0207 | P4 | crew | Wire chapter-writer Agent skills=["./skills/technical-writer"] in its factory | test_chapter_writer_skills_wired asserts technical-writer skill path present in agent.skills | todo
T-0208 | P4 | crew | Implement figure/data Agent factory in crew/agents/figure_agent.py with allow_delegation=False | test_figure_agent_built asserts role mentions figure/data and allow_delegation is False | todo
T-0209 | P4 | crew | Implement Hebrew BiDi-chapter writer Agent factory in crew/agents/bidi_writer.py | test_bidi_writer_built asserts role references Hebrew/BiDi and skills include technical-writer | todo
T-0210 | P4 | crew | Implement editor/reviewer Agent factory in crew/agents/editor.py with allow_delegation=False | test_editor_agent_built asserts role mentions editor/review and allow_delegation is False | todo
T-0211 | P4 | crew | Implement latex-author Agent factory in crew/agents/latex_author.py wiring skills=["./skills/latex-author"] | test_latex_author_skills_wired asserts latex-author skill path present in agent.skills | todo
T-0212 | P4 | crew | Inject the provider-agnostic LLM instance (from providers loader) into every agent factory via an llm param | test_agents_receive_llm asserts each factory passes the injected llm object onto the Agent, never a hardcoded model string | todo
T-0213 | P4 | crew | Ensure no agent factory hardcodes the model name "gemini/gemini-2.5-flash" anywhere | test_no_hardcoded_model greps agents/ source and asserts the literal model string is absent | todo
T-0214 | P4 | crew | Add docstrings and type hints to every public agent factory signature | ruff/pydocstyle check clean and test_agent_factories_typed asserts return annotation is Agent | todo
T-0215 | P4 | crew | Create crew/tools.py defining the read-local-PDF tool wrapping reference/Agent_Architecture_2026.pdf path from config | test_pdf_tool_reads_reference asserts tool returns mocked PDF text and path comes from config | todo
T-0216 | P4 | crew | Add a file-write tool in crew/tools.py for persisting outputs under output/ with path from config | test_write_tool_persists asserts tool writes to a tmp output dir resolved from config, not a hardcoded path | todo
T-0217 | P4 | crew | Add a web/search research tool stub in crew/tools.py that is fully mockable (no live network) | test_search_tool_mocked asserts the tool delegates to an injected client that is mocked in the test | todo
T-0218 | P4 | crew | Confirm CodeInterpreterTool is NOT imported or referenced in crew/tools.py | test_no_code_interpreter_tool greps tools.py and asserts CodeInterpreterTool string is absent | todo
T-0219 | P4 | crew | Expose a tools registry/getter in crew/tools.py returning the tool list for a given agent role | test_tools_registry_by_role asserts researcher role yields pdf+search tools and latex_author yields write tool | todo
T-0220 | P4 | crew | Keep crew/tools.py under the 150-line cap, splitting helpers into crew/tools_helpers.py if needed | scripts/check_line_cap.py passes for crew/tools.py and any helper module | todo
T-0221 | P4 | crew | Add type hints + docstrings on all public tool functions/classes in crew/tools.py | ruff clean and test_tools_typed asserts each public tool has a return annotation | todo
T-0222 | P4 | skills | Create src/cosmos77_ex03/skills/researcher/SKILL.md with YAML frontmatter name+description selector | test_researcher_skill_frontmatter parses YAML and asserts name=="researcher" and description non-empty | todo
T-0223 | P4 | skills | Write the researcher SKILL.md Markdown body describing source-gathering + citation extraction workflow | test_researcher_skill_body asserts body mentions citations and reference PDF usage | todo
T-0224 | P4 | skills | Create src/cosmos77_ex03/skills/technical-writer/SKILL.md with YAML frontmatter name+description | test_technical_writer_skill_frontmatter asserts name=="technical-writer" and description present | todo
T-0225 | P4 | skills | Write the technical-writer SKILL.md body covering chapter structure, tables, formulas, BiDi guidance | test_technical_writer_skill_body asserts body references tabularx/amsmath and BiDi | todo
T-0226 | P4 | skills | Create src/cosmos77_ex03/skills/latex-author/SKILL.md with YAML frontmatter name+description | test_latex_author_skill_frontmatter asserts name=="latex-author" and description present | todo
T-0227 | P4 | skills | Write the latex-author SKILL.md body covering LuaLaTeX preamble, biblatex+biber, hyperref-last rules | test_latex_author_skill_body asserts body mentions lualatex, biber, and hyperref ordering | todo
T-0228 | P4 | skills | Validate all three SKILL.md frontmatters are well-formed YAML with exactly name+description keys | test_all_skills_frontmatter_keys asserts each frontmatter has only name and description keys | todo
T-0229 | P4 | skills | Add a skills loader/util in shared/ to resolve skill paths and assert they exist on disk | test_skill_paths_resolve asserts each of the 3 skill dirs and SKILL.md files exist | todo
T-0230 | P4 | skills | Ensure skill directory names exactly match the names referenced in agent factories | test_skill_names_match_agents asserts agent skills= paths map 1:1 to existing skill dir names | todo
T-0231 | P4 | tests | Create tests/conftest.py fixtures that mock crewai Agent/Task/Crew so no live LLM/CrewAI calls occur | test suite runs with `uv run pytest` offline; conftest provides agent/crew mock fixtures | todo
T-0232 | P4 | tests | Add a fixture providing a fake provider-agnostic llm object for injection into agent factories | test_llm_fixture_available asserts the fixture returns a sentinel llm reused across agent tests | todo
T-0233 | P4 | tests | Assert every agent factory is constructed without performing any network or Gemini API call | test_agents_no_live_calls patches crewai.Agent and asserts the real LLM client is never invoked | todo
T-0234 | P4 | tests | Add deterministic test ensuring chapter-writer factory output is stable for the same chapter input | test_chapter_writer_deterministic asserts two builds with same input produce equal config | todo
T-0235 | P4 | tests | Write a test that the tools registry returns deterministic ordering for a given role | test_tools_registry_deterministic asserts repeated calls return identically ordered tool lists | todo
T-0236 | P4 | tests | Add tests covering crew/tools.py PDF tool error path when the reference file is missing | test_pdf_tool_missing_file asserts a clear error/exception is raised (mocked filesystem) | todo
T-0237 | P4 | tests | Ensure P4 modules contribute to coverage >=85% with a focused pytest --cov on crew/ and skills loader | `uv run pytest --cov=cosmos77_ex03.crew` reports >=85% for the P4 surface | todo
T-0238 | P4 | crew | Add crew/agents/__init__.py registry mapping role keys to factory callables for the assembler (P5) | test_agent_registry_complete asserts all 7 role keys (researcher,planner,chapter_writer,figure,bidi_writer,editor,latex_author) are present | todo
T-0239 | P4 | crew | Read agent role/goal/backstory text from config/setup.json (or a crew config section) not literals | test_agent_text_from_config asserts changing config value changes the built agent's goal | todo
T-0240 | P4 | config | Add an "agents" section to config/setup.json with role/goal/backstory per agent | test_setup_json_has_agents asserts setup.json parses and contains all 7 agent entries | todo
T-0241 | P4 | config | Add a "tools" section to config (reference_pdf path, output_dir) consumed by crew/tools.py | test_setup_json_has_tools asserts reference_pdf and output_dir keys exist and are strings | todo
T-0242 | P4 | crew | Implement a shared base/helper to avoid duplicated Agent kwargs across factories (OOP no-duplication) | test_agent_common_kwargs asserts all factories route through one helper applying shared defaults | todo
T-0243 | P4 | crew | Ensure all chapter-writer tasks are intended for async_execution (factory exposes async-capable flag/hint) | test_chapter_writer_async_hint asserts the factory marks chapters as async-eligible per ADR-002 | todo
T-0244 | P4 | crew | Add token-usage hook plumbing point so agents/tasks can later surface result.token_usage | test_token_usage_accessor asserts a helper exists to read token_usage from a mocked result object | todo
T-0245 | P4 | qa | Add scripts/check_line_cap.py invocation over all new P4 .py files to enforce the 150-line cap | running check_line_cap.py over crew/ and skills loader exits 0 | todo
T-0246 | P4 | qa | Run ruff over all P4-created modules and fix to zero findings | `uv run ruff check src/cosmos77_ex03/crew` reports zero issues | todo
T-0247 | P4 | crew | Guard against Arabic characters in any skill/agent text (language rule: Arabic forbidden) | test_no_arabic_in_skills greps the 3 SKILL.md files and asserts no Arabic Unicode range chars | todo
T-0248 | P4 | crew | Provide an editor agent goal emphasizing citation/link/BiDi/table/formula correctness (B15 alignment) | test_editor_goal_mentions_qa asserts editor goal references citations, links, and BiDi | todo
T-0249 | P4 | crew | Provide latex-author agent backstory referencing the exact LaTeX stack (babel bidi, fontspec, biblatex) | test_latex_author_backstory_stack asserts backstory mentions babel and biblatex | todo
T-0250 | P4 | docs | Append P4 prompt log entry recording this session's agent/skill/tool decisions | docs prompt log file gains a P4 dated entry; test/grep confirms the P4 marker present | todo
T-0251 | P4 | docs | Update docs/TODO.md to reference the P4 task IDs once this part is enumerated | TODO.md contains a P4 section linking docs/_todo_parts/P4.txt | todo
T-0252 | P5 | tasks | Create src/cosmos77_ex03/crew/tasks/research_task.py defining the research Task assigned to the researcher agent | file exists and ruff passes on it | todo
T-0253 | P5 | tasks | Set research_task description to instruct mining reference/Agent_Architecture_2026.pdf plus the article topic for agent architecture, orchestration, and governance facts | description string references the topic and the local PDF path | todo
T-0254 | P5 | tasks | Set research_task expected_output to a structured Markdown research brief covering all 12 planned chapter themes | expected_output string enumerates the 12 chapter themes | todo
T-0255 | P5 | tasks | Wire research_task output_file to output/research.md so CrewAI persists the brief | task.output_file == "output/research.md" asserted in a test | todo
T-0256 | P5 | tasks | Keep research_task.py under the 150-line hard cap by delegating long prompt text to a separate prompt module | scripts/check_line_cap.py reports research_task.py <= 150 lines | todo
T-0257 | P5 | tasks | Create src/cosmos77_ex03/crew/prompts/research_prompts.py holding the research description/expected_output template strings | file exists and is imported by research_task.py | todo
T-0258 | P5 | tasks | Load the article topic and lecturer/course metadata for prompts from config/setup.json instead of hardcoding | test asserts prompt text is built from setup.json values | todo
T-0259 | P5 | tasks | Create src/cosmos77_ex03/crew/tasks/outline_task.py defining the outline Task assigned to the outline-planner agent | file exists and ruff passes on it | todo
T-0260 | P5 | tasks | Set outline_task to depend on research_task via context=[research_task] so the outline consumes the research brief | test asserts research_task is in outline_task.context | todo
T-0261 | P5 | tasks | Set outline_task expected_output to a JSON object with exactly 12 chapter entries each having id, title, summary, and is_hebrew_bidi fields | expected_output schema text lists those four fields and the count 12 | todo
T-0262 | P5 | tasks | Flag exactly one of the 12 chapters with is_hebrew_bidi=true in the outline prompt instructions | prompt text instructs exactly one Hebrew BiDi chapter | todo
T-0263 | P5 | tasks | Wire outline_task output_file to output/outline.json for the machine-readable outline | task.output_file == "output/outline.json" asserted in a test | todo
T-0264 | P5 | tasks | Create src/cosmos77_ex03/crew/prompts/outline_prompts.py holding the outline description/expected_output template strings | file exists and imported by outline_task.py | todo
T-0265 | P5 | tasks | Create src/cosmos77_ex03/shared/outline_schema.py with a typed dataclass/Pydantic model for ChapterSpec (id, title, summary, is_hebrew_bidi) | file exists with type hints on all fields | todo
T-0266 | P5 | tasks | Add an OutlineDocument model wrapping a list[ChapterSpec] plus article title and validating exactly 12 chapters | model raises on != 12 chapters in a unit test | todo
T-0267 | P5 | tasks | Add validation in OutlineDocument that exactly one ChapterSpec has is_hebrew_bidi=true | model raises when zero or two BiDi chapters present | todo
T-0268 | P5 | shared | Create src/cosmos77_ex03/shared/outline_writer.py that serializes an OutlineDocument to output/outline.json with stable key ordering | function writes deterministic JSON asserted byte-equal in a test | todo
T-0269 | P5 | shared | Add a render_outline_markdown function producing output/outline.md from an OutlineDocument with numbered chapters | function output contains 12 numbered headings in a test | todo
T-0270 | P5 | shared | Mark the Hebrew BiDi chapter in the rendered outline.md with an explicit "(Hebrew BiDi)" label | rendered markdown contains the BiDi label exactly once | todo
T-0271 | P5 | shared | Create src/cosmos77_ex03/shared/citations_model.py with a Citation model (key, title, author, year, url/source) | file exists with type hints and a bibkey field | todo
T-0272 | P5 | shared | Add a CitationsCollection model that rejects duplicate citation keys | model raises on duplicate keys in a unit test | todo
T-0273 | P5 | shared | Create src/cosmos77_ex03/shared/citations_writer.py serializing a CitationsCollection to output/citations.json deterministically | function writes stable-ordered JSON asserted in a test | todo
T-0274 | P5 | tasks | Have outline_task also emit citation seeds gathered during research into the outline JSON for downstream bib generation | expected_output text requests a citations array of keyed sources | todo
T-0275 | P5 | shared | Add a function extract_citations_from_outline that reads outline JSON and writes output/citations.json | unit test feeds sample outline JSON and checks citations.json contents | todo
T-0276 | P5 | sdk | Add SDK.research() to src/cosmos77_ex03/sdk/sdk.py that runs the research+outline tasks and returns paths to research.md, outline.json, outline.md, citations.json | method signature and return type documented with type hints | todo
T-0277 | P5 | sdk | Make SDK.research() build the Crew with researcher and outline-planner agents plus research_task and outline_task in Process.sequential | test asserts the crew tasks list order researcher-then-outline | todo
T-0278 | P5 | sdk | Have SDK.research() record result.token_usage into the gatekeeper cost meter for the Spec Sheet | test asserts cost meter received a token_usage entry tagged "research" | todo
T-0279 | P5 | sdk | Ensure SDK.research() validates the produced outline via OutlineDocument before returning, raising on schema violations | test asserts a malformed crew output causes SDK.research() to raise | todo
T-0280 | P5 | sdk | Keep sdk.py under 150 lines by delegating research orchestration to a helper in src/cosmos77_ex03/sdk/research_runner.py | scripts/check_line_cap.py reports sdk.py <= 150 lines | todo
T-0281 | P5 | sdk | Create src/cosmos77_ex03/sdk/research_runner.py encapsulating crew assembly and output validation for the research phase | file exists and imported by sdk.py | todo
T-0282 | P5 | tasks | Ensure research_task and outline_task read the active LLM via the provider-agnostic loader, never a hardcoded model string | grep for "gemini/" in tasks/ returns no matches | todo
T-0283 | P5 | tasks | Set async_execution=False on research_task and outline_task since they are sequential dependencies, reserving async for chapter writers | test asserts async_execution is False on both tasks | todo
T-0284 | P5 | tasks | Set allow_delegation=False posture by assigning tasks only to their named agents with no delegation context | test asserts each task.agent matches the intended worker | todo
T-0285 | P5 | tests | Add tests/test_research_task.py asserting research_task description, expected_output, agent, and output_file with the LLM fully mocked | pytest tests/test_research_task.py passes with no live calls | todo
T-0286 | P5 | tests | Add tests/test_outline_task.py asserting outline_task context, expected_output schema text, agent, and output_file | pytest tests/test_outline_task.py passes | todo
T-0287 | P5 | tests | Add tests/test_outline_schema.py covering ChapterSpec, OutlineDocument 12-chapter rule, and the single-BiDi-chapter rule | pytest tests/test_outline_schema.py passes with all branches | todo
T-0288 | P5 | tests | Add tests/test_outline_writer.py checking deterministic outline.json bytes and outline.md heading rendering | pytest tests/test_outline_writer.py passes | todo
T-0289 | P5 | tests | Add tests/test_citations_model.py covering Citation, duplicate-key rejection, and citations.json serialization | pytest tests/test_citations_model.py passes | todo
T-0290 | P5 | tests | Add tests/test_extract_citations.py feeding sample outline JSON and asserting output/citations.json structure | pytest tests/test_extract_citations.py passes | todo
T-0291 | P5 | tests | Add tests/test_sdk_research.py with the Crew.kickoff mocked, asserting returned file paths and cost-meter recording | pytest tests/test_sdk_research.py passes with mocked crew | todo
T-0292 | P5 | tests | Mock all CrewAI/Gemini I/O in P5 tests via a shared fixture in tests/conftest.py so no network calls occur | test suite runs offline; fixture patches Crew.kickoff and the LLM | todo
T-0293 | P5 | tests | Add a deterministic sample outline JSON fixture under tests/fixtures/sample_outline.json for reuse across P5 tests | fixture file exists and loads in tests | todo
T-0294 | P5 | qa | Add scripts/qa_outline.py validating output/outline.json against OutlineDocument and reporting pass/fail | running script on a valid outline exits 0, on invalid exits nonzero | todo
T-0295 | P5 | qa | Have qa_outline.py assert exactly 12 chapters and exactly one is_hebrew_bidi=true entry | script prints the BiDi chapter id and chapter count | todo
T-0296 | P5 | qa | Add a citations cross-check in qa_outline.py ensuring every outline citation seed key appears in output/citations.json | script flags any missing citation key | todo
T-0297 | P5 | config | Add P5 entries to config/setup.json declaring research output paths (research.md, outline.json, outline.md, citations.json) | setup.json contains an outputs.research block with the four paths | todo
T-0298 | P5 | config | Add the 12-chapter count and Hebrew-BiDi requirement as configurable constraints in config/setup.json | tasks read chapter_count and bidi_chapter_count from setup.json | todo
T-0299 | P5 | docs | Update docs/TODO.md marking P5 research/outline task IDs and link them to this P5.txt enumeration | TODO.md references the P5 task IDs | todo
T-0300 | P5 | ci | Run ruff check and scripts/check_line_cap.py over all new P5 modules and confirm zero violations | ruff reports zero issues and line-cap script exits 0 | todo
T-0301 | P5 | ci | Run coverage for the P5 modules and confirm combined coverage stays >= 85% | pytest --cov reports >= 85% for crew/tasks, shared, and sdk research code | todo
T-0302 | P6 | crew | Create src/cosmos77_ex03/crew/chapter_writer.py defining a build_chapter_agent(role, provider) factory returning a CrewAI Agent for one chapter | chapter_writer.py exists, exports build_chapter_agent, and `uv run python -c "from cosmos77_ex03.crew.chapter_writer import build_chapter_agent"` succeeds | todo
T-0303 | P6 | crew | Wire the chapter-writer agent's skills=["./skills/technical-writer"] and goal/backstory from config, never hardcoding the model | grep finds skills="./skills/technical-writer" and no literal "gemini" string in chapter_writer.py | todo
T-0304 | P6 | crew | Set allow_delegation=False and max_rpm from setup.json on the chapter-writer agent | test_chapter_writer_agent_no_delegation asserts agent.allow_delegation is False and max_rpm matches config | todo
T-0305 | P6 | crew | Add a build_chapter_writers(outline, provider) helper producing one Agent per outline chapter | test asserts len(build_chapter_writers(outline)) == number of chapters in the outline fixture | todo
T-0306 | P6 | tests | Add tests/unit/test_chapter_writer.py with the Agent constructor and LLM fully mocked (no live calls) | `uv run pytest tests/unit/test_chapter_writer.py -m "not live"` passes with mocked Agent | todo
T-0307 | P6 | crew | Create src/cosmos77_ex03/crew/write_tasks.py defining build_write_task(chapter, agent) returning a Task with async_execution=True | write_tasks.py exists and test asserts the returned Task has async_execution True | todo
T-0308 | P6 | crew | Make build_write_task set output_file to output/chapters/ch_NN.md using zero-padded two-digit index | test_write_task_output_path asserts output_file == "output/chapters/ch_03.md" for chapter index 3 | todo
T-0309 | P6 | crew | Compose the per-chapter task description from the chapter's outline title and bullet points without hardcoding chapter content | test asserts the task description contains the outline chapter title and each bullet string | todo
T-0310 | P6 | crew | Set expected_output on each write task to a Markdown chapter spec (heading + prose + citation placeholders) | grep finds expected_output mentioning "Markdown" and "##" heading guidance in write_tasks.py | todo
T-0311 | P6 | crew | Add build_write_tasks(outline, agents) mapping each chapter to one async write Task | test asserts len(build_write_tasks(outline, agents)) equals chapter count and all have async_execution True | todo
T-0312 | P6 | tests | Add tests/unit/test_write_tasks.py covering output paths, async flag, and description templating with mocked Task | `uv run pytest tests/unit/test_write_tasks.py` passes and covers build_write_task and build_write_tasks | todo
T-0313 | P6 | crew | Create src/cosmos77_ex03/crew/bidi_writer.py defining build_bidi_agent(provider) for the single Hebrew-English BiDi chapter | bidi_writer.py exists and exports build_bidi_agent | todo
T-0314 | P6 | crew | Configure the BiDi agent's skills and instruction to emit interleaved Hebrew+English and forbid Arabic | grep finds "Hebrew" and "Arabic" prohibition text in bidi_writer.py | todo
T-0315 | P6 | crew | Add build_bidi_task(agent) returning a non-async Task whose output_file is the designated Hebrew chapter ch_NN.md | test asserts the bidi task output_file points at the configured Hebrew chapter file | todo
T-0316 | P6 | crew | Ensure exactly one chapter is routed through bidi_writer while all others use chapter_writer | test_only_one_bidi_chapter asserts exactly one bidi task and the rest are standard write tasks | todo
T-0317 | P6 | tests | Add tests/unit/test_bidi_writer.py asserting Hebrew-content instruction, single-chapter selection, and Arabic prohibition (mocked) | `uv run pytest tests/unit/test_bidi_writer.py` passes | todo
T-0318 | P6 | tests | Add a test asserting no Arabic-range characters appear in any bidi_writer prompt/instruction string | test_bidi_prompt_has_no_arabic scans instruction text for U+0600..U+06FF and asserts none present | todo
T-0319 | P6 | crew | Create src/cosmos77_ex03/crew/editor_task.py defining build_editor_agent(provider) for the editor/reviewer | editor_task.py exists and exports build_editor_agent | todo
T-0320 | P6 | crew | Define build_editor_task(agent, write_tasks) with context set to all chapter write tasks so it runs after them | test asserts the editor Task.context contains every write task instance | todo
T-0321 | P6 | crew | Set the editor task output_file to output/article.md and async_execution=False (it aggregates) | test_editor_output asserts output_file == "output/article.md" and async_execution is False | todo
T-0322 | P6 | crew | Have the editor task description instruct merging chapters in order, fixing flow, and preserving citation keys | grep finds "merge"/"order" and "citation" guidance in editor_task.py expected_output/description | todo
T-0323 | P6 | tests | Add tests/unit/test_editor_task.py covering context wiring, output path, and aggregation instruction (mocked) | `uv run pytest tests/unit/test_editor_task.py` passes | todo
T-0324 | P6 | shared | Add src/cosmos77_ex03/shared/chapter_paths.py with chapter_md_path(index) -> Path for output/chapters/ch_NN.md | test asserts chapter_md_path(7) == Path("output/chapters/ch_07.md") | todo
T-0325 | P6 | shared | Ensure chapter_paths.py creates the output/chapters/ directory on demand without overwriting existing files | test_ensure_chapters_dir asserts the directory is created and pre-existing files are untouched | todo
T-0326 | P6 | tests | Add tests/unit/test_chapter_paths.py covering zero-padding, Path type, and directory creation | `uv run pytest tests/unit/test_chapter_paths.py` passes | todo
T-0327 | P6 | crew | Add a crew assembly function build_writing_crew(outline, provider) returning a Crew with writers + bidi + editor, Process.sequential | test asserts the Crew.process is sequential and agents include writers, bidi, and editor | todo
T-0328 | P6 | crew | Pass max_rpm from setup.json into the Crew (and/or agents) to throttle Gemini request rate | test_crew_max_rpm asserts the Crew/agent max_rpm equals config crew.max_rpm | todo
T-0329 | P6 | crew | Order tasks so async write tasks precede the editor task in the Crew task list | test asserts the editor task index is greater than all write task indices in the assembled Crew | todo
T-0330 | P6 | tests | Add tests/unit/test_writing_crew.py asserting agent/task composition, sequential process, and max_rpm with Crew mocked | `uv run pytest tests/unit/test_writing_crew.py` passes | todo
T-0331 | P6 | sdk | Implement SDK.write_chapters(outline=None) in src/cosmos77_ex03/sdk/sdk.py replacing the NotImplementedError stub | grep confirms write_chapters has a body and the prior NotImplementedError is gone | todo
T-0332 | P6 | sdk | Have write_chapters load outline from output/outline.json when no outline argument is provided | test asserts write_chapters() reads output/outline.json via a mocked loader when called with no args | todo
T-0333 | P6 | sdk | Build the writing crew inside write_chapters and invoke crew.kickoff() (mocked) to run chapter generation | test_write_chapters_kickoff asserts crew.kickoff is called exactly once with mocks | todo
T-0334 | P6 | sdk | Persist the editor result to output/article.md from write_chapters and return its path | test asserts output/article.md is written and write_chapters returns that Path (using a tmp path fixture) | todo
T-0335 | P6 | sdk | Record result.token_usage from the kickoff into the run/spec-sheet accumulator inside write_chapters | test asserts the mocked token_usage is forwarded to the cost-meter/accumulator | todo
T-0336 | P6 | sdk | Return per-chapter file paths (output/chapters/ch_NN.md list) plus article.md from write_chapters | test asserts the returned structure lists every chapter path and the article path | todo
T-0337 | P6 | tests | Add tests/unit/test_sdk_write_chapters.py with crew, kickoff, filesystem, and outline-loader all mocked | `uv run pytest tests/unit/test_sdk_write_chapters.py` passes with zero live calls | todo
T-0338 | P6 | sdk | Validate that write_chapters errors clearly when output/outline.json is missing or malformed | test_write_chapters_missing_outline asserts a clear ValueError/FileNotFoundError is raised | todo
T-0339 | P6 | crew | Create src/cosmos77_ex03/crew/retry.py with a with_retry(callable, attempts, backoff) wrapper for transient LLM/rate-limit errors | retry.py exists and exports with_retry | todo
T-0340 | P6 | crew | Make with_retry read attempts and backoff seconds from setup.json (no hardcoded numbers) | grep shows retry params sourced from config and test asserts they match setup.json | todo
T-0341 | P6 | crew | Have with_retry re-raise after exhausting attempts and not swallow non-retryable errors | test_retry_exhausts asserts the original exception propagates after the configured attempt count | todo
T-0342 | P6 | crew | Make with_retry retry only on designated transient exceptions (rate-limit/timeout) and pass through others immediately | test asserts a non-transient error is raised on first try without retry | todo
T-0343 | P6 | crew | Apply with_retry around the crew.kickoff call in the SDK write_chapters path | test asserts kickoff is retried on a simulated transient error and succeeds on the second mocked attempt | todo
T-0344 | P6 | tests | Add tests/unit/test_retry.py covering success-first-try, retry-then-succeed, exhaust, and passthrough with time.sleep patched (no real wall-clock delay) | `uv run pytest tests/unit/test_retry.py` passes deterministically and asserts sleep is mocked | todo
T-0345 | P6 | config | Ensure setup.json carries crew.max_rpm, crew.retry.attempts, and crew.retry.backoff_seconds keys | `uv run python -c "import json;d=json.load(open('config/setup.json'));assert d['crew']['retry']['attempts']"` exits 0 | todo
T-0346 | P6 | cli | Add a `write-chapters` CLI subcommand in cli/main.py invoking SDK.write_chapters() | `uv run cosmos77-ex03 write-chapters --help` exits 0 and lists the command | todo
T-0347 | P6 | tests | Add tests/unit/test_cli_write_chapters.py invoking the command via CliRunner with SDK mocked | `uv run pytest tests/unit/test_cli_write_chapters.py` passes and asserts SDK.write_chapters called once | todo
T-0348 | P6 | qa | Enforce the 150-line cap on every new P6 module via scripts/check_line_cap.py | `uv run python scripts/check_line_cap.py` exits 0 with all crew/sdk/shared files under 150 lines | todo
T-0349 | P6 | qa | Run ruff across the P6 modules and tests with zero findings | `uv run ruff check src tests` reports no issues | todo
T-0350 | P6 | qa | Confirm coverage stays >=85% after adding P6 modules and tests | `uv run pytest --cov=src/cosmos77_ex03 -m "not live"` reports total coverage >= 85% | todo
T-0351 | P6 | docs | Update docs/TODO.md marking P6 chapter-writing tasks and add a conventional commit referencing P6 task IDs | git log shows a "feat(crew): parallel chapter writing" commit referencing P6 IDs and TODO.md reflects P6 status | todo
T-0352 | P7 | figures | Create src/cosmos77_ex03/figures/charts.py module skeleton with module docstring and typed public functions | file src/cosmos77_ex03/figures/charts.py exists and imports without error | todo
T-0353 | P7 | figures | Add matplotlib import using the non-interactive Agg backend at module top of charts.py | grep shows matplotlib.use('Agg') set before pyplot import in charts.py | todo
T-0354 | P7 | figures | Read figure output paths and styling from config (config/setup.json figures section) not hardcoded literals | charts.py contains no hardcoded output paths; values resolved via config loader | todo
T-0355 | P7 | config | Add a "figures" block to config/setup.json with output_dir, adoption_pdf, frameworks_pdf, dpi, figsize keys | config/setup.json parses as JSON and contains figures.output_dir and both pdf filenames | todo
T-0356 | P7 | figures | Define build_adoption_chart(data, out_path) producing a bar/line chart of AI-agent adoption over time | function build_adoption_chart defined with type hints and docstring in charts.py | todo
T-0357 | P7 | figures | Define build_frameworks_chart(data, out_path) comparing agent frameworks by a quantitative metric | function build_frameworks_chart defined with type hints and docstring in charts.py | todo
T-0358 | P7 | figures | Provide deterministic default datasets for adoption and frameworks charts in config or a data constants module | datasets are fixed constants (no random, no network); repeated runs yield identical input data | todo
T-0359 | P7 | figures | Set fixed figure size and DPI from config in both chart builders for reproducible output dimensions | both builders call plt.figure/savefig with figsize and dpi pulled from config | todo
T-0360 | P7 | figures | Save adoption chart as vector/raster PDF to output/figures/adoption.pdf via savefig(format implied by .pdf) | running make_figures creates output/figures/adoption.pdf with non-zero size | todo
T-0361 | P7 | figures | Save frameworks chart as PDF to output/figures/frameworks.pdf | running make_figures creates output/figures/frameworks.pdf with non-zero size | todo
T-0362 | P7 | figures | Close matplotlib figures (plt.close(fig)) after savefig to avoid state leakage across builders | charts.py calls plt.close after each savefig; no open-figure warnings in test output | todo
T-0363 | P7 | figures | Add axis labels, title, and legend to adoption chart for B5 readability | adoption builder sets ax.set_xlabel/set_ylabel/set_title and legend; verified in test via Axes inspection | todo
T-0364 | P7 | figures | Add axis labels, title, and legend to frameworks chart for B5 readability | frameworks builder sets labels/title/legend; verified in test via Axes inspection | todo
T-0365 | P7 | figures | Set a deterministic matplotlib rcParams seed/style (fixed font, no timestamp metadata) for byte-stable PDFs | charts.py sets rcParams and pdf metadata CreationDate to a fixed value | todo
T-0366 | P7 | figures | Suppress embedded timestamp in PDF metadata so re-runs are reproducible | generated PDFs have stable/empty CreationDate verified by inspecting metadata in test | todo
T-0367 | P7 | figures | Ensure output/figures/ directory is created if missing before saving | make_figures creates output/figures path via mkdir(parents=True, exist_ok=True) | todo
T-0368 | P7 | figures | Keep charts.py under the 150-line hard cap, splitting helpers into figures/chart_data.py if needed | python scripts/check_line_cap.py passes for all figures/*.py | todo
T-0369 | P7 | sdk | Add SDK.make_figures() method to src/cosmos77_ex03/sdk/sdk.py delegating to figures module | method SDK.make_figures defined with type hints and docstring | todo
T-0370 | P7 | sdk | Have make_figures() return the list of generated figure paths for downstream LaTeX use | make_figures returns [adoption_pdf_path, frameworks_pdf_path] as Path objects | todo
T-0371 | P7 | sdk | Route make_figures() output locations through the same config the CLI/build uses (no duplicate path logic) | make_figures reads figures config once via shared loader; no inline path strings in sdk.py | todo
T-0372 | P7 | sdk | Ensure make_figures() is idempotent (overwrites existing PDFs without error on repeated calls) | calling make_figures twice succeeds and yields identical files | todo
T-0373 | P7 | sdk | Keep sdk.py under 150-line cap after adding make_figures (extract logic into figures module) | python scripts/check_line_cap.py passes for sdk/sdk.py | todo
T-0374 | P7 | latex | Create src/cosmos77_ex03/figures/diagram_tikz.tex containing a standalone TikZ architecture diagram for B4 | file figures/diagram_tikz.tex exists and contains a tikzpicture environment | todo
T-0375 | P7 | latex | Design the TikZ diagram to depict agent orchestration (researcher->planner->writers->editor->latex-author) | diagram_tikz.tex includes labeled nodes and arrows matching the crew pipeline | todo
T-0376 | P7 | latex | Use TikZ libraries (positioning, arrows.meta, shapes) declared via \usetikzlibrary in the diagram or preamble | \usetikzlibrary directives present; diagram references named arrow tips/shapes | todo
T-0377 | P7 | latex | Make diagram_tikz.tex an \input-able fragment (no document preamble) referenced from a section/figure | file contains only tikzpicture markup suitable for \input, no \documentclass | todo
T-0378 | P7 | latex | Create src/cosmos77_ex03/latex/table.tex with a tabularx+booktabs table that does not overflow margins for B6 | file latex/table.tex exists with tabularx using \linewidth and booktabs rules | todo
T-0379 | P7 | latex | Populate table.tex with a meaningful comparison (e.g. frameworks vs features) sized to text width | table uses X columns so content wraps; \toprule/\midrule/\bottomrule present | todo
T-0380 | P7 | latex | Add a \caption and \label to the table.tex float for cross-referencing and TOC of tables | table.tex contains \caption and \label{tab:...} | todo
T-0381 | P7 | latex | Create src/cosmos77_ex03/latex/formula.tex with an amsmath display equation (not flat text) for B7 | file latex/formula.tex exists using equation/align with \label{eq:...} | todo
T-0382 | P7 | latex | Make formula.tex a non-trivial fancy formula (sum/integral/fraction/matrix) demonstrating amsmath | formula.tex uses at least one of \sum \int \frac \begin{matrix} or aligned terms | todo
T-0383 | P7 | latex | Ensure table.tex and formula.tex are \input fragments without preamble for inclusion in sections | neither file contains \documentclass; both compile when input into main.tex | todo
T-0384 | P7 | latex | Wire \includegraphics of adoption.pdf and frameworks.pdf into a figures section fragment | a section fragment references both generated PDFs via \includegraphics with width | todo
T-0385 | P7 | tests | Write a failing test (red) tests/test_charts.py::test_make_figures_creates_pdfs asserting both PDFs exist | test exists and initially fails before implementation, passes after | todo
T-0386 | P7 | tests | Mock matplotlib savefig in a test verifying builders are invoked with config-derived paths | test asserts savefig called with output/figures/adoption.pdf and frameworks.pdf | todo
T-0387 | P7 | tests | Add deterministic test asserting two consecutive make_figures runs produce byte-identical PDFs | test_charts.py::test_figures_deterministic compares file hashes equal | todo
T-0388 | P7 | tests | Add test that generated PDF files start with the %PDF magic header | test reads first bytes of adoption.pdf/frameworks.pdf and asserts b'%PDF' prefix | todo
T-0389 | P7 | tests | Add test that build_adoption_chart sets expected axis labels/title on a real (Agg) Axes | test inspects returned/created Axes and asserts label strings | todo
T-0390 | P7 | tests | Add test that build_frameworks_chart sets expected axis labels/title on Axes | test inspects Axes and asserts label/title strings | todo
T-0391 | P7 | tests | Add SDK test tests/test_sdk_make_figures.py asserting make_figures returns both Path objects | test asserts return value list length 2 and paths end with the configured filenames | todo
T-0392 | P7 | tests | Add test that make_figures creates output/figures dir when absent (use tmp_path) | test points config at tmp_path, asserts directory and files created | todo
T-0393 | P7 | tests | Ensure all P7 tests run with NO live LLM/CrewAI/lualatex calls (matplotlib local only, others mocked) | grep of test files shows no network/Crew calls; pytest runs offline | todo
T-0394 | P7 | tests | Add test validating diagram_tikz.tex contains a tikzpicture and required \usetikzlibrary lines | test reads diagram_tikz.tex and asserts substrings present | todo
T-0395 | P7 | tests | Add test validating table.tex uses tabularx with \linewidth and booktabs macros | test reads table.tex and asserts 'tabularx' '\linewidth' '\toprule' present | todo
T-0396 | P7 | tests | Add test validating formula.tex uses an amsmath display environment with a label | test reads formula.tex and asserts equation/align and \label present | todo
T-0397 | P7 | qa | Add a QA check (scripts/qa_pdf.py hook) confirming adoption.pdf and frameworks.pdf are valid non-empty PDFs | qa_pdf.py reports both figure PDFs present and parseable | todo
T-0398 | P7 | docs | Update docs/TODO.md to mark P7 figure/table/formula tasks and link this P7.txt breakdown | docs/TODO.md references P7 figures/charts/diagram/table/formula items | todo
T-0399 | P7 | ci | Confirm ruff passes with zero findings on figures/charts.py and sdk.py changes | uv run ruff check src reports zero errors for new/modified files | todo
T-0400 | P7 | ci | Confirm coverage for figures module and make_figures stays >=85% after P7 tests | uv run pytest --cov shows figures/charts.py coverage >=85% | todo
T-0401 | P7 | docs | Make a conventional commit for P7 referencing the relevant TODO IDs (feat(figures): ...) | git log shows a feat(figures) commit message citing P7 task IDs | todo
T-0402 | P8 | latex | Create tex/preamble.tex with documentclass[12pt,a4paper]{article} as the first line | test_preamble_documentclass_first asserts the first non-comment line is the \documentclass directive | todo
T-0403 | P8 | latex | Add babel[bidi=basic, layout=tabular, english, hebrew] plus \babelprovide for english(main) and hebrew to tex/preamble.tex | test_preamble_babel_bidi asserts the babel load line and both \babelprovide lines are present | todo
T-0404 | P8 | latex | Declare \babelfont{rm}{FreeSerif} with commented macOS Arial Hebrew and David CLM fallbacks in tex/preamble.tex | test_preamble_babelfont asserts FreeSerif babelfont line exists and fallback lines are present but commented | todo
T-0405 | P8 | latex | Load amsmath+amssymb, booktabs+tabularx, graphicx, tikz with shapes.geometric/arrows.meta/positioning libraries in tex/preamble.tex | test_preamble_core_packages asserts each of these \usepackage/\usetikzlibrary lines is present | todo
T-0406 | P8 | latex | Load biblatex[backend=biber, style=numeric, sorting=none] and \addbibresource{refs.bib} in tex/preamble.tex | test_preamble_biblatex asserts the biblatex options and \addbibresource{refs.bib} are present | todo
T-0407 | P8 | latex | Load hyperref[colorlinks=true,...,unicode=true] as the LAST \usepackage in tex/preamble.tex | test_preamble_hyperref_last asserts hyperref is the final \usepackage line and includes unicode=true | todo
T-0408 | P8 | latex | Configure fancyhdr in tex/preamble.tex: \pagestyle{fancy}, \leftmark header L, \thepage header R, fixed course footer C | test_preamble_fancyhdr asserts \pagestyle{fancy}, \leftmark, \thepage, and the footer course string are present | todo
T-0409 | P8 | latex | Add \hypersetup pdftitle/pdfauthor metadata lines to tex/preamble.tex | test_preamble_hypersetup asserts \hypersetup with pdftitle and pdfauthor keys is present | todo
T-0410 | P8 | latex | Verify tex/preamble.tex contains no Arabic Unicode-range characters | test_preamble_no_arabic greps preamble.tex and asserts no codepoints in U+0600..U+06FF | todo
T-0411 | P8 | latex | Create tex/main.tex skeleton that \input{preamble} then opens \begin{document} | test_main_inputs_preamble asserts \input{preamble} precedes \begin{document} in main.tex | todo
T-0412 | P8 | latex | Add a titlepage cover block in tex/main.tex with placeholder tokens for title/author/course/instructor and \today date | test_main_titlepage_tokens asserts the titlepage env exists and contains the four substitution tokens plus \today | todo
T-0413 | P8 | latex | Add \tableofcontents followed by \newpage after the cover in tex/main.tex | test_main_has_toc asserts \tableofcontents and a following \newpage appear after \end{titlepage} | todo
T-0414 | P8 | latex | Emit \input{sections/ch_NN} lines for num_chapters from config/setup.json in tex/main.tex (no hardcoded count) | test_main_inputs_match_config asserts the count of \input{sections/...} lines equals setup.json num_chapters | todo
T-0415 | P8 | latex | Add \printbibliography[title={References / ביבליוגרפיה}] before \end{document} in tex/main.tex | test_main_printbibliography asserts the \printbibliography line with the BiDi title precedes \end{document} | todo
T-0416 | P8 | config | Add an "article" section to config/setup.json with title, author, course, instructor keys for cover binding | test_setup_json_article_keys asserts setup.json parses and contains all four article keys as strings | todo
T-0417 | P8 | latex | Create src/cosmos77_ex03/latex/assemble.py exporting an assemble_article callable | test_assemble_importable asserts `from cosmos77_ex03.latex.assemble import assemble_article` imports cleanly | todo
T-0418 | P8 | latex | Implement cover-token substitution in assemble.py reading title/author/course/instructor from config | test_assemble_cover_substitution asserts rendered main.tex contains config article values, not placeholder tokens | todo
T-0419 | P8 | latex | Escape LaTeX-special characters (ampersand, %, _, #) in substituted cover values inside assemble.py | test_assemble_escapes_ampersand asserts a course name with "&" renders as "\&" in the output main.tex | todo
T-0420 | P8 | latex | Implement per-chapter section emission in assemble.py writing one tex/sections/ch_NN.tex per output/chapters/ch_NN.md | test_assemble_writes_sections asserts one ch_NN.tex file written per input md (mocked tmp dirs) | todo
T-0421 | P8 | latex | Wrap each assembled section body with a \section{<chapter title>} header sourced from outline.json | test_assemble_section_header asserts each ch_NN.tex begins with \section{ and the outline title text | todo
T-0422 | P8 | latex | Resolve all input/output paths in assemble.py (chapters dir, sections dir, refs.bib, main.tex) from config not literals | test_assemble_paths_from_config asserts changing a config path changes where assemble.py reads/writes | todo
T-0423 | P8 | latex | Implement refs.bib generation in assemble.py from output/citations.json | test_assemble_generates_refsbib asserts tex/refs.bib is written from a mocked citations.json | todo
T-0424 | P8 | latex | Emit a valid biblatex @entry per citation in refs.bib with key, title, author, year fields | test_refsbib_entry_fields asserts each generated entry has a cite key and the expected required fields | todo
T-0425 | P8 | latex | Ensure refs.bib cite keys are unique and deterministic for identical citations.json input | test_refsbib_deterministic asserts two runs over the same citations.json produce byte-identical refs.bib | todo
T-0426 | P8 | latex | Handle empty/missing citations.json gracefully in assemble.py (emit empty-but-valid refs.bib) | test_assemble_empty_citations asserts an empty citations list yields a refs.bib with zero entries and no crash | todo
T-0427 | P8 | latex | Escape special characters and strip stray braces in bib field values during refs.bib generation | test_refsbib_escapes_fields asserts a title containing "&"/"%" is escaped in the emitted entry | todo
T-0428 | P8 | latex | Return a structured AssembleResult (sections written, bib entries, main.tex path) from assemble_article | test_assemble_result_shape asserts the result exposes section_count, bib_count, and main_path | todo
T-0429 | P8 | latex | Keep src/cosmos77_ex03/latex/assemble.py under the 150-line cap, splitting bib/cover helpers if needed | scripts/check_line_cap.py reports assemble.py (and any helper) <= 150 lines | todo
T-0430 | P8 | latex | Factor shared LaTeX-escaping into a single helper reused by cover and bib paths (OOP no-duplication) | test_escape_helper_single_source asserts both cover and bib escaping call one shared escape function | todo
T-0431 | P8 | latex | Add docstrings and full type hints to every public function/class in assemble.py | ruff/pydocstyle clean and test_assemble_typed asserts public signatures carry return annotations | todo
T-0432 | P8 | crew | Create src/cosmos77_ex03/crew/tasks_latex.py defining the md->LaTeX-per-section Task factory | test_tasks_latex_importable asserts `from cosmos77_ex03.crew.tasks_latex import build_latex_task` imports cleanly | todo
T-0433 | P8 | crew | build_latex_task parameterized by chapter id/title binds the chapter markdown into the task description | test_latex_task_per_chapter asserts distinct tasks for two chapter ids carry their respective md content | todo
T-0434 | P8 | crew | Set the latex task expected_output to instruct emitting ONLY LaTeX (no markdown fences, no prose preamble) | test_latex_task_expected_output asserts expected_output mentions "only LaTeX" and forbids markdown fences | todo
T-0435 | P8 | crew | Assign each latex task to the latex-author agent via the agent param | test_latex_task_agent asserts the task.agent is the latex-author agent (mocked factory) | todo
T-0436 | P8 | crew | Source the latex task description/expected_output template text from config, not hardcoded strings | test_latex_task_text_from_config asserts editing the config template changes the built task description | todo
T-0437 | P8 | crew | Add a post-process sanitizer that strips ```latex fences and leading prose from an LLM section result | test_strip_latex_fences asserts a fenced/prefixed mocked output is reduced to pure LaTeX | todo
T-0438 | P8 | crew | Keep crew/tasks_latex.py under the 150-line cap, splitting the sanitizer if needed | scripts/check_line_cap.py reports tasks_latex.py (and any helper) <= 150 lines | todo
T-0439 | P8 | crew | Confirm crew/tasks_latex.py does not hardcode the model name or import CodeInterpreterTool | test_tasks_latex_clean greps the file and asserts no model literal and no CodeInterpreterTool reference | todo
T-0440 | P8 | crew | Add docstrings and type hints to the public task factory and sanitizer in tasks_latex.py | ruff clean and test_tasks_latex_typed asserts the factory returns a Task annotation | todo
T-0441 | P8 | sdk | Add SDK.assemble_latex() to src/cosmos77_ex03/sdk/sdk.py as the single entry point for assembly | test_sdk_has_assemble_latex asserts callable(SDK.assemble_latex) | todo
T-0442 | P8 | sdk | SDK.assemble_latex reads chapters/outline/citations from output/ and delegates to latex.assemble | test_sdk_assemble_calls_assemble asserts assemble_article invoked once with config-derived paths (mock) | todo
T-0443 | P8 | sdk | SDK.assemble_latex returns the AssembleResult (sections, bib entries, main.tex path) to the caller | test_sdk_assemble_result asserts returned result exposes section_count, bib_count, and main_path | todo
T-0444 | P8 | sdk | SDK.assemble_latex raises a clear error when required output/ inputs (chapters or citations) are missing | test_sdk_assemble_missing_inputs asserts FileNotFoundError/RuntimeError with an explanatory message | todo
T-0445 | P8 | sdk | Keep sdk.py within the 150-line cap by delegating assembly logic to the latex module/helper | scripts/check_line_cap.py reports sdk.py <= 150 lines | todo
T-0446 | P8 | cli | Add an "assemble" subcommand to the CLI that invokes SDK.assemble_latex and prints a summary | test_cli_assemble_invokes_sdk asserts SDK.assemble_latex called once and stdout reports section/bib counts (mock) | todo
T-0447 | P8 | tests | Add conftest fixtures providing mocked output/ inputs (chapters md, outline.json, citations.json) in a tmp dir | fixture importable and yields a tmp output tree consumed by assemble tests with no live I/O | todo
T-0448 | P8 | tests | Mock crewai Task/Agent so building latex tasks performs zero live LLM/CrewAI calls | test_tasks_latex_no_live_calls asserts crewai.Task is patched and no Gemini client is invoked | todo
T-0449 | P8 | qa | Run ruff over latex/assemble.py, crew/tasks_latex.py, and the sdk assemble helper to zero findings | `uv run ruff check src/cosmos77_ex03/latex src/cosmos77_ex03/crew/tasks_latex.py` reports zero issues | todo
T-0450 | P8 | qa | Ensure P8 modules contribute coverage >=85% via focused pytest --cov on latex/ and tasks_latex | `uv run pytest --cov=cosmos77_ex03.latex` reports >=85% for the P8 surface | todo
T-0451 | P8 | docs | Append a P8 prompt-log entry and link the P8 task IDs from docs/TODO.md | docs/prompts gains a dated P8 entry and TODO.md contains a P8 section referencing docs/_todo_parts/P8.txt | todo
T-0452 | P9 | config | Add a "build" section to config/setup.json declaring engine "lualatex", bib backend "biber", and pass count 3 | config/setup.json parses as JSON and contains build.engine == "lualatex", build.bib_backend == "biber", build.passes == 3 | todo
T-0453 | P9 | config | Add config/setup.json keys main_tex ("tex/main.tex") and build_dir ("tex/") consumed by build_pdf.sh and SDK | both keys present and read in a test test_build_config_keys_present | todo
T-0454 | P9 | config | Add config/setup.json qa.expected_pages range (min 13, max 17) for the ~15-page B1 check | qa.expected_pages.min and .max present; test_qa_page_range_config asserts 13<=min and max<=17 | todo
T-0455 | P9 | config | Add config/setup.json qa.required_strings list (cover title, author, course, lecturer) for cover/B2 text assertions | list non-empty; test_qa_required_strings_config asserts title string present | todo
T-0456 | P9 | scripts | Create scripts/build_pdf.sh with shebang and set -euo pipefail running lualatex->biber->lualatex->lualatex | file exists, is executable (chmod +x verified by test), grep finds the 4-step order | todo
T-0457 | P9 | scripts | Make build_pdf.sh read engine/main_tex/build_dir from config/setup.json via a small python -c helper, not hardcoded | grep build_pdf.sh shows no literal "lualatex" before config read; ruff/shellcheck-style review passes | todo
T-0458 | P9 | scripts | Make build_pdf.sh cd into build_dir and invoke biber on the jobname (main) between lualatex passes | grep shows "biber main" (or jobname var) sequenced after first lualatex | todo
T-0459 | P9 | scripts | Make build_pdf.sh exit non-zero if any lualatex/biber step fails (propagate via set -e) | test_build_script_fails_on_error uses a fake failing step and asserts non-zero exit | todo
T-0460 | P9 | scripts | Make build_pdf.sh echo the resolved output path tex/main.pdf on success for capture by SDK | grep shows echo of main.pdf path; test parses last stdout line == expected pdf path | todo
T-0461 | P9 | scripts | Add build_pdf.sh -halt-on-error and -interaction=nonstopmode flags to lualatex invocations | grep build_pdf.sh shows both flags on each lualatex call | todo
T-0462 | P9 | sdk | Add SDK.build_pdf() in src/cosmos77_ex03/sdk/sdk.py delegating to a BuildRunner in src/cosmos77_ex03/latex/ | test_sdk_build_pdf_delegates asserts BuildRunner.run called once | todo
T-0463 | P9 | sdk | Add SDK.qa_pdf() delegating to a PdfQa class in src/cosmos77_ex03/latex/ returning a QaReport | test_sdk_qa_pdf_delegates asserts PdfQa.run called once and report returned | todo
T-0464 | P9 | sdk | Give SDK.build_pdf() and SDK.qa_pdf() docstrings and type hints (return BuildResult/QaReport) | ruff clean; test_sdk_build_qa_signatures asserts annotations present via inspect | todo
T-0465 | P9 | latex | Create src/cosmos77_ex03/latex/build_runner.py wrapping subprocess invocation of scripts/build_pdf.sh | file exists, under 150 lines, importable as cosmos77_ex03.latex.build_runner | todo
T-0466 | P9 | latex | BuildRunner.run() must subprocess.run the script with cwd=repo root and capture stdout/stderr | test_build_runner_invokes_script mocks subprocess.run and asserts script path + cwd | todo
T-0467 | P9 | latex | BuildRunner.run() returns BuildResult(returncode, pdf_path, stdout, stderr) dataclass | test_build_result_fields asserts dataclass fields and types | todo
T-0468 | P9 | latex | BuildRunner must raise BuildError when returncode != 0 with stderr tail in message | test_build_runner_raises_on_nonzero asserts BuildError raised and stderr included | todo
T-0469 | P9 | latex | BuildRunner resolves script path and main.pdf path from config, never hardcoded literals | test_build_runner_uses_config monkeypatches config and asserts resolved paths | todo
T-0470 | P9 | latex | Split BuildResult/BuildError into src/cosmos77_ex03/latex/build_types.py to keep build_runner under the line cap | both files under 150 lines per check_line_cap.py; import works | todo
T-0471 | P9 | qa | Create src/cosmos77_ex03/latex/pdf_qa.py PdfQa class running the §13.1 checklist over tex/main.pdf | file exists, under 150 lines, importable as cosmos77_ex03.latex.pdf_qa | todo
T-0472 | P9 | qa | PdfQa.check_pages() counts PDF pages and validates against qa.expected_pages range | test_qa_pages_in_range passes with mocked page count 15; fails at 5 | todo
T-0473 | P9 | qa | PdfQa.check_required_strings() extracts text and asserts cover/B2 strings present | test_qa_required_strings mocks text extraction and asserts all strings found | todo
T-0474 | P9 | qa | PdfQa.check_toc() verifies a Table of Contents entry exists in the PDF outline/text | test_qa_toc_present mocks outline and asserts TOC detected | todo
T-0475 | P9 | qa | PdfQa.check_links() verifies hyperref link/annotation count > 0 (clickable citations B9) | test_qa_links_present mocks annotations and asserts count>0 | todo
T-0476 | P9 | qa | PdfQa.check_bibliography() asserts a References/Bibliography heading and >=1 resolved citation marker | test_qa_bibliography mocks text and asserts heading + citation found | todo
T-0477 | P9 | qa | PdfQa.check_no_undefined_refs() scans build log for "??" / "undefined references" and fails if present | test_qa_undefined_refs_fail feeds a log with "??" and asserts failure | todo
T-0478 | P9 | qa | PdfQa.check_hebrew_present() asserts at least one Hebrew codepoint range char in extracted text (B8) | test_qa_hebrew_present mocks text with Hebrew and asserts pass | todo
T-0479 | P9 | qa | PdfQa.check_no_arabic() fails if any Arabic codepoint range char appears anywhere (canon: Arabic forbidden) | test_qa_no_arabic feeds Arabic char and asserts failure; clean text passes | todo
T-0480 | P9 | qa | PdfQa.check_image_present() asserts >=1 embedded image/XObject (TikZ diagram B4) | test_qa_image_present mocks XObject list and asserts count>=1 | todo
T-0481 | P9 | qa | PdfQa.check_overfull() parses build log for "Overfull \hbox" warnings and reports count (table fit B6) | test_qa_overfull_count mocks log with one warning and asserts count==1 | todo
T-0482 | P9 | qa | PdfQa.run() aggregates all checks into QaReport(passed:bool, results:list[CheckResult]) | test_qa_run_aggregates asserts overall passed reflects worst sub-check | todo
T-0483 | P9 | qa | Define CheckResult/QaReport dataclasses in src/cosmos77_ex03/latex/qa_types.py with name/passed/detail | test_qa_types_fields asserts fields and that QaReport.passed is all(results) | todo
T-0484 | P9 | qa | PdfQa reads page extraction backend (pypdf) path/import from shared util, mockable in tests | test_qa_uses_mockable_reader monkeypatches reader and asserts no real file read | todo
T-0485 | P9 | qa | QaReport.to_json() serializes results for inclusion in output/spec_sheet.json QA section | test_qa_report_to_json round-trips and contains each check name | todo
T-0486 | P9 | cli | Add CLI subcommand "build" in src/cosmos77_ex03/cli/ that calls SDK.build_pdf() and prints pdf path | test_cli_build_invokes_sdk mocks SDK and asserts build_pdf called, exit 0 | todo
T-0487 | P9 | cli | Add CLI subcommand "qa" that calls SDK.qa_pdf() and prints the QaReport summary | test_cli_qa_invokes_sdk mocks SDK and asserts qa_pdf called, summary printed | todo
T-0488 | P9 | cli | CLI "qa" exits non-zero when QaReport.passed is False (gate semantics) | test_cli_qa_nonzero_on_fail asserts SystemExit code != 0 when report failed | todo
T-0489 | P9 | cli | CLI "build" exits non-zero and prints stderr tail when BuildError is raised | test_cli_build_nonzero_on_error asserts exit != 0 and error message printed | todo
T-0490 | P9 | cli | Wire build and qa subcommands into the existing argparse/click dispatcher with help text | test_cli_help_lists_build_qa asserts "build" and "qa" appear in --help output | todo
T-0491 | P9 | tests | Add tests/latex/test_build_runner.py mocking subprocess.run for all BuildRunner paths | file exists; pytest collects and passes; no live lualatex invoked | todo
T-0492 | P9 | tests | Add tests/latex/test_pdf_qa.py mocking pypdf reader and log file for all PdfQa checks | file exists; pytest passes; no real PDF parsed against live file | todo
T-0493 | P9 | tests | Add tests/cli/test_cli_build_qa.py covering build/qa subcommands and exit codes | file exists; pytest passes; SDK mocked | todo
T-0494 | P9 | tests | Add a fixture providing a fake build log string with Overfull and undefined-ref samples | fixture importable; used by overfull and undefined-ref tests; tests deterministic | todo
T-0495 | P9 | tests | Add a fixture providing fake extracted-text with Hebrew, cover strings, and citation markers | fixture used by required_strings/hebrew/bibliography tests; deterministic | todo
T-0496 | P9 | tests | Assert no test in tests/latex or tests/cli performs a live lualatex/biber subprocess (RULE: mock all I/O) | grep over new tests shows subprocess/Popen only via mock; CI check passes | todo
T-0497 | P9 | tests | Verify combined coverage for latex/ and cli/ build+qa modules >= 85% | pytest --cov reports >=85% for the new modules; gate passes | todo
T-0498 | P9 | ci | Add scripts/check_line_cap.py assertion run over new latex/cli files (<=150 lines each) | check_line_cap.py exits 0 for build_runner.py, pdf_qa.py, qa_types.py, build_types.py | todo
T-0499 | P9 | ci | Run ruff over new P9 modules and tests with zero findings | ruff check src/cosmos77_ex03/latex tests/latex tests/cli exits 0 | todo
T-0500 | P9 | docs | Add docs/MANUAL_EYEBALL.md checklist (cover, TOC, headers, image, graph, table, formula, BiDi, citations) for the human gate | file exists with one checkbox per B1-B9 acceptance item | todo
T-0501 | P9 | docs | Document the build+qa workflow (uv run ... build; uv run ... qa) in README.md and reference §13.1 | README contains a "Build & QA" section naming the build/qa CLI commands and the gate | todo
T-0502 | P10 | spec | Run the full pipeline end-to-end and serialize the accumulated CostMeter snapshot to output/spec_sheet.json | output/spec_sheet.json exists and is valid JSON loadable via json.load without error | todo
T-0503 | P10 | spec | Ensure output/spec_sheet.json top-level contains tokens, latency, cost, memory keys from CostMeter.to_spec_sheet() | `python -c "import json;d=json.load(open('output/spec_sheet.json'));assert {'tokens','latency','cost','memory'}<=set(d)"` exits 0 | todo
T-0504 | P10 | spec | Record active provider name and resolved model id into output/spec_sheet.json from config/providers.json | spec_sheet.json contains provider="gemini" and model="gemini/gemini-2.5-flash" matching providers.json active block | todo
T-0505 | P10 | spec | Break tokens into prompt_tokens, completion_tokens, total_tokens in output/spec_sheet.json | total_tokens equals prompt_tokens + completion_tokens asserted by test_spec_sheet_token_sum | todo
T-0506 | P10 | spec | Record per-agent token attribution map in output/spec_sheet.json keyed by agent role | spec_sheet.json has agents block with one entry per crew agent and integer token counts | todo
T-0507 | P10 | spec | Record total wall-clock latency seconds and per-stage latency breakdown in output/spec_sheet.json | latency.total_seconds is a positive float and latency.stages has research/write/figures/assemble/build keys | todo
T-0508 | P10 | spec | Record estimated USD cost computed from total tokens and the per-1k rate in config in output/spec_sheet.json | cost.usd equals round(total_tokens/1000*rate,6) verified by test_spec_sheet_cost_matches_rate | todo
T-0509 | P10 | spec | Record peak RSS memory in MB sampled by the gatekeeper into output/spec_sheet.json | memory.peak_rss_mb is a positive number asserted by test_spec_sheet_memory_present | todo
T-0510 | P10 | spec | Stamp package version 1.00, run timestamp (ISO 8601), and total LLM call count into output/spec_sheet.json | spec_sheet.json has version=="1.00", a parseable run_timestamp, and integer call_count | todo
T-0511 | P10 | spec | Add scripts/qa_spec_sheet.py validating output/spec_sheet.json against the expected schema | running the script on the committed spec_sheet exits 0 and on a malformed file exits nonzero | todo
T-0512 | P10 | tests | Add tests/qa/test_spec_sheet_schema.py asserting all required keys and types in output/spec_sheet.json | pytest tests/qa/test_spec_sheet_schema.py passes against a fixture spec sheet | todo
T-0513 | P10 | tests | Mock the gatekeeper snapshot so test_spec_sheet_generation runs without live LLM/CrewAI calls | test patches CostMeter.to_spec_sheet and asserts written JSON matches the mocked payload | todo
T-0514 | P10 | docs | Replace the placeholder README.md with the full HW3 lab report exceeding 250 lines | `wc -l README.md` reports >= 250 lines | todo
T-0515 | P10 | docs | Write a README title block stating topic, both author names, date, course UOH-RL07, and lecturer Dr. Yoram Segal | README.md header contains the topic string, both authors, the course code, and the lecturer name | todo
T-0516 | P10 | docs | Add a README project-overview section summarizing the CrewAI + LaTeX article generator goal | README.md has an Overview/Introduction section describing the multi-agent article pipeline | todo
T-0517 | P10 | docs | Embed at least three images in README.md using Markdown image syntax | `grep -c '!\[' README.md` reports >= 3 image references | todo
T-0518 | P10 | docs | Ensure every README image path resolves to a committed file under assets/ or output/figures/ | a link-check confirms each README image src file exists on disk | todo
T-0519 | P10 | figures | Export the crew architecture diagram to assets/architecture.png for embedding in the README | assets/architecture.png exists and is a valid PNG (file header check passes) | todo
T-0520 | P10 | figures | Export a pipeline/data-flow diagram (research to PDF) to assets/pipeline.png for the README | assets/pipeline.png exists and is referenced by README.md | todo
T-0521 | P10 | figures | Export a cover or compiled-PDF screenshot to assets/cover_preview.png for the README | assets/cover_preview.png exists and is referenced by README.md | todo
T-0522 | P10 | docs | Add a README architecture section describing agents, sequential+async process, and ADR-002 rationale | README.md Architecture section names researcher, outline-planner, chapter-writers, figure agent, BiDi writer, editor, latex-author | todo
T-0523 | P10 | docs | Add a B1-B9 acceptance-to-page-map table mapping each criterion to the page/section in tex/main.pdf | README.md contains a Markdown table with one row per B1..B9 and a page or section reference column | todo
T-0524 | P10 | docs | Verify each page number in the B1-B9 map matches the actual page in tex/main.pdf | a manual cross-check note confirms B1-B9 page references are within the compiled PDF page count | todo
T-0525 | P10 | docs | Add a README Quickstart section with uv sync, .env setup, and the article generation command | README.md Quickstart shows `uv sync`, copying .env.example, and `uv run cosmos77-article` invocation | todo
T-0526 | P10 | docs | Document the end-to-end CLI flow research to write to figures to assemble to build to qa in README | README.md lists each CLI subcommand in pipeline order with a one-line purpose | todo
T-0527 | P10 | docs | Add a README config-swap section showing how to change the active provider in config/providers.json | README.md shows editing the active field to swap Gemini for Groq/OpenAI and updating the api_key_env | todo
T-0528 | P10 | docs | State in README that the model is never hardcoded and is read from config/providers.json | README.md config section explicitly notes zero hardcoded model and points to providers.json | todo
T-0529 | P10 | docs | Add a README Spec Sheet section that embeds and interprets the output/spec_sheet.json numbers | README.md presents the tokens, latency, cost, and memory values with a sentence interpreting each | todo
T-0530 | P10 | docs | Keep README Spec Sheet figures consistent with the committed output/spec_sheet.json values | the token/cost/latency numbers quoted in README.md match output/spec_sheet.json exactly | todo
T-0531 | P10 | docs | Add a README LaTeX-stack section listing LuaLaTeX, babel bidi, biblatex+biber, hyperref last | README.md documents the compile chain lualatex -> biber -> lualatex -> lualatex | todo
T-0532 | P10 | docs | Add a README CrewAI Skills section listing latex-author, technical-writer, researcher skills | README.md names the three skills and their SKILL.md location under src/cosmos77_ex03/skills/ | todo
T-0533 | P10 | docs | Add a README repository-layout tree covering sdk, shared, providers, crew, skills, figures, latex, cli | README.md includes a directory tree matching the actual src/cosmos77_ex03 subpackages | todo
T-0534 | P10 | docs | Add a README testing section documenting mocked LLM/CrewAI tests and the >=85% coverage gate | README.md states all LLM I/O is mocked and shows the pytest --cov command and 85% threshold | todo
T-0535 | P10 | docs | Add a README self-assessment section claiming a score of 85 with per-criterion justification | README.md self-assessment states 85 and lists B1-B15 with a short justification each | todo
T-0536 | P10 | docs | Tabulate the B1-B15 self-assessment as a Markdown table with criterion, status, and evidence columns | README.md contains a B1-B15 table with 15 data rows and an evidence link/section per row | todo
T-0537 | P10 | docs | Add a README BiDi note pointing to the single Hebrew-English chapter and confirming no Arabic | README.md states exactly one Hebrew BiDi chapter and that Arabic is absent project-wide | todo
T-0538 | P10 | docs | Add a README prerequisites section for system deps (uv, MacTeX/TeX Live full, Hebrew font) | README.md lists uv, LuaLaTeX+biber, and a Hebrew-capable font as system prerequisites | todo
T-0539 | P10 | docs | Add a README license and authorship footer crediting both students under MIT 2026 | README.md footer states MIT (c) 2026 with both author names and links LICENSE | todo
T-0540 | P10 | docs | Add a README link to docs/PRD.md, docs/PLAN.md, and docs/TODO.md | README.md contains working relative links to the three docs files | todo
T-0541 | P10 | qa | Add scripts/qa_readme.py asserting README.md line count >= 250 and image count >= 3 | running scripts/qa_readme.py exits 0 on the final README and nonzero if either threshold fails | todo
T-0542 | P10 | qa | Extend qa_readme.py to verify the B1-B9 page-map table and B1-B15 self-assessment table are present | qa_readme.py flags a missing acceptance or self-assessment table | todo
T-0543 | P10 | qa | Extend qa_readme.py to verify every README image and doc link target file exists on disk | qa_readme.py reports any broken image or document link as a failure | todo
T-0544 | P10 | tests | Add tests/qa/test_readme.py invoking qa_readme.py logic on README.md | pytest tests/qa/test_readme.py passes confirming line count, images, and tables | todo
T-0545 | P10 | tests | Add a test asserting README config-swap snippet keys match config/providers.json field names | test parses providers.json and asserts active and api_key_env appear in the README snippet | todo
T-0546 | P10 | config | Add config/setup.json entries declaring spec_sheet output path and the per-1k token cost rate | setup.json has outputs.spec_sheet path and a cost.rate_per_1k numeric value | todo
T-0547 | P10 | config | Add README asset paths (architecture, pipeline, cover_preview) as configurable constants in setup.json | setup.json lists the three README asset paths under an assets block | todo
T-0548 | P10 | docs | Update docs/TODO.md marking the P10 README and spec-sheet task IDs against this enumeration | docs/TODO.md references the P10 task IDs and links to docs/_todo_parts/P10.txt | todo
T-0549 | P10 | ci | Run ruff check over all new P10 scripts and modules and confirm zero violations | `uv run ruff check` reports zero issues for qa_spec_sheet.py and qa_readme.py | todo
T-0550 | P10 | ci | Run scripts/check_line_cap.py over P10 modules confirming no .py exceeds 150 lines | check_line_cap.py exits 0 for all P10 Python files | todo
T-0551 | P10 | ci | Run pytest with coverage for P10 modules and confirm combined coverage stays >= 85% | `uv run pytest --cov` reports >= 85% including the new qa and spec-sheet tests | todo
T-0552 | P11 | qa | Run ruff check across src/ scripts/ tests/ and fix every lint violation | command `uv run ruff check src scripts tests` exits 0 with no findings | todo
T-0553 | P11 | qa | Run ruff format --check across the repo and reformat any non-conforming files | command `uv run ruff format --check .` reports all files already formatted | todo
T-0554 | P11 | qa | Execute scripts/check_line_cap.py over all .py files to enforce the 150-line hard cap | command `uv run python scripts/check_line_cap.py` exits 0 listing zero offenders | todo
T-0555 | P11 | tests | Run the full pytest suite and confirm every test passes with no skips that hide failures | command `uv run pytest` reports all passed and exit code 0 | todo
T-0556 | P11 | tests | Run pytest with coverage and assert the total is >=85 percent | command `uv run pytest --cov=cosmos77_ex03 --cov-fail-under=85` exits 0 | todo
T-0557 | P11 | tests | Generate an HTML/term coverage report and record per-module gaps below 85 percent | file output/coverage_report.txt exists and lists any module under threshold | todo
T-0558 | P11 | tests | Add tests covering any module surfaced under 85 percent until each crosses threshold | re-run `uv run pytest --cov --cov-fail-under=85` passes after additions | todo
T-0559 | P11 | tests | Verify no test performs a live LLM/CrewAI/Gemini/lualatex call by grepping for unmocked clients | grep over tests/ shows all such calls wrapped in mock/patch fixtures | todo
T-0560 | P11 | tests | Assert determinism by running the suite twice and diffing results | two consecutive `uv run pytest -p no:randomly` runs produce identical pass sets | todo
T-0561 | P11 | qa | Confirm pyproject.toml pins version 1.00 and no module disagrees | grep `version = "1.00"` present in pyproject.toml and __init__ matches | todo
T-0562 | P11 | docs | Create docs/ACCEPTANCE.md with a B1-B15 traceability table header (criterion/file/test/page/status) | file docs/ACCEPTANCE.md exists with a 5-column table header | todo
T-0563 | P11 | docs | Document B1 (~15 pages) row mapping to tex/main.pdf with measured page count | ACCEPTANCE.md B1 row cites pdfinfo page count and status PASS | todo
T-0564 | P11 | docs | Document B2 (cover) row mapping to scripts/generate_cover_pdf.py and tex/main.tex title block | ACCEPTANCE.md B2 row names cover file/test and status | todo
T-0565 | P11 | docs | Document B3 (TOC + chapters + running headers/footers) row mapping to preamble fancyhdr config | ACCEPTANCE.md B3 row names tex/preamble.tex and a qa_pdf check | todo
T-0566 | P11 | docs | Document B4 (TikZ diagram image) row mapping to tex/figures/ and its test | ACCEPTANCE.md B4 row names the figure source and verifying test | todo
T-0567 | P11 | docs | Document B5 (matplotlib-generated PDF graph) row mapping to src/.../figures generator | ACCEPTANCE.md B5 row names the figure script and output PDF | todo
T-0568 | P11 | docs | Document B6 (non-overflow table) row mapping to the tabularx/booktabs section and overflow check | ACCEPTANCE.md B6 row names section file and qa_pdf overflow check | todo
T-0569 | P11 | docs | Document B7 (amsmath display formula) row mapping to the formula section | ACCEPTANCE.md B7 row names section file and formula test | todo
T-0570 | P11 | docs | Document B8 (Hebrew-English BiDi chapter) row mapping to the BiDi chapter section | ACCEPTANCE.md B8 row names the BiDi section and BiDi test | todo
T-0571 | P11 | docs | Document B9 (clickable resolved citations) row mapping to refs.bib + biblatex/biber config | ACCEPTANCE.md B9 row names refs.bib and a citation-resolution check | todo
T-0572 | P11 | docs | Document B10 (real CrewAI multi-agent team) row mapping to src/.../crew and crew tests | ACCEPTANCE.md B10 row names crew module and an agent test | todo
T-0573 | P11 | docs | Document B11 (tex/ project committed + builds) row mapping to scripts/build_pdf.sh | ACCEPTANCE.md B11 row names build script and a build smoke test | todo
T-0574 | P11 | docs | Document B12 (provider-agnostic config + Spec Sheet) row mapping to config/providers.json + spec_sheet.json | ACCEPTANCE.md B12 row names both files and a spec-sheet test | todo
T-0575 | P11 | docs | Document B13 (CrewAI Skills) row mapping to src/.../skills/*/SKILL.md | ACCEPTANCE.md B13 row names the three SKILL.md files | todo
T-0576 | P11 | docs | Document B14 (PRD/PLAN/TODO/README docs) row mapping to docs/ and README.md | ACCEPTANCE.md B14 row confirms each doc file exists | todo
T-0577 | P11 | docs | Document B15 (technical-wrapper correctness) row mapping to scripts/qa_pdf.py aggregate | ACCEPTANCE.md B15 row names qa_pdf.py and lists its sub-checks | todo
T-0578 | P11 | qa | Cross-link each ACCEPTANCE.md row to a real existing test name and verify the test exists | every test name cited in ACCEPTANCE.md resolves via `uv run pytest --collect-only` | todo
T-0579 | P11 | qa | Perform a full clean run from scratch deleting output/ and tex build artifacts first | rm output build dirs then full pipeline regenerates them without error | todo
T-0580 | P11 | latex | Run the lualatex->biber->lualatex->lualatex sequence and confirm tex/main.pdf builds clean | scripts/build_pdf.sh exits 0 and tex/main.pdf is produced | todo
T-0581 | P11 | latex | Scan the LaTeX build log for unresolved references and undefined citations | grep of tex/main.log shows no "undefined" or "There were undefined references" | todo
T-0582 | P11 | qa | Run scripts/qa_pdf.py against the freshly built PDF and confirm all assertions pass | command `uv run python scripts/qa_pdf.py tex/main.pdf` exits 0 | todo
T-0583 | P11 | qa | Verify the PDF page count is within the ~15-page target band via pdfinfo | qa_pdf.py page-count assertion passes for 13-17 pages | todo
T-0584 | P11 | qa | Verify hyperref links and citation anchors resolve clickably in the PDF | qa_pdf.py link-resolution check reports zero dangling internal links | todo
T-0585 | P11 | qa | Verify no table overflows the text block in the built PDF | qa_pdf.py overflow check reports zero Overfull \hbox over tolerance in tables | todo
T-0586 | P11 | qa | Verify the BiDi Hebrew chapter renders right-to-left correctly in the PDF | qa_pdf.py BiDi check confirms Hebrew glyphs present and RTL ordered | todo
T-0587 | P11 | qa | Verify Arabic text appears nowhere in sources or the rendered PDF | grep for Arabic Unicode range over tex/ output/ returns nothing | todo
T-0588 | P11 | qa | Run a secrets scan over the repo for API keys and tokens | secrets scan (gitleaks/grep patterns) reports zero findings | todo
T-0589 | P11 | qa | Confirm .env is gitignored and no real key is committed anywhere | `git check-ignore .env` succeeds and grep for api_key values in tracked files is empty | todo
T-0590 | P11 | config | Confirm config/providers.json contains no inline secrets only api_key_env names | grep over providers.json finds env-var names not key literals | todo
T-0591 | P11 | qa | Confirm the active provider model is read from config not hardcoded in any .py | grep for "gemini/gemini-2.5-flash" string literal in src returns nothing | todo
T-0592 | P11 | ci | Assemble a single QA gauntlet script chaining ruff, format, line-cap, pytest-cov, qa_pdf, secrets | scripts/qa_gauntlet.sh exists and exits 0 running all stages in order | todo
T-0593 | P11 | ci | Make qa_gauntlet.sh fail fast and print which stage failed | running with an injected failure stops at that stage with a named error | todo
T-0594 | P11 | qa | Confirm both authors appear in git shortlog with non-zero commit counts | `git shortlog -sne` lists both student authors and excludes Claude co-author | todo
T-0595 | P11 | qa | Confirm commits follow conventional-commit format and reference TODO IDs | `git log --oneline` shows type-prefixed subjects citing PNN/TODO IDs | todo
T-0596 | P11 | qa | Verify the prompt log for the session exists and is current | docs/prompt_log (session file) exists and includes P11 entries | todo
T-0597 | P11 | qa | Verify the gatekeeper cost meter recorded token usage into spec_sheet.json | output/spec_sheet.json contains non-null tokens/latency/cost/memory fields | todo
T-0598 | P11 | qa | Reproducibility check: clone-style fresh `uv sync` and rerun gauntlet in a clean dir | `uv sync` then qa_gauntlet.sh exits 0 in a pristine checkout | todo
T-0599 | P11 | docs | Update docs/TODO.md to mark all P11 task IDs complete after each passes | TODO.md P11 entries flipped from todo to done with no orphans | todo
T-0600 | P11 | docs | Add a Reproducibility section to README.md documenting the exact gauntlet commands | README.md lists `uv sync`, qa_gauntlet.sh, and build_pdf.sh steps | todo
T-0601 | P11 | qa | Final sign-off: confirm every B1-B15 row in ACCEPTANCE.md shows status PASS | ACCEPTANCE.md contains no row with status FAIL or TODO | todo
T-0602 | P12 | config | Add a "cover" block to config/setup.json holding exercise_number, self_score, ex03_repo_url, course, lecturer, author, topic, date fields | config/setup.json parses as valid JSON and contains cover.exercise_number=3 and cover.self_score=85 | todo
T-0603 | P12 | config | Set cover.exercise_number to integer 3 in config/setup.json | python -c "import json;assert json.load(open('config/setup.json'))['cover']['exercise_number']==3" exits 0 | todo
T-0604 | P12 | config | Set cover.self_score to integer 85 in config/setup.json | python assertion on cover.self_score==85 passes | todo
T-0605 | P12 | config | Set cover.ex03_repo_url to the GitHub ex03 repository URL in config/setup.json | the URL string starts with https://github.com/ and is non-empty | todo
T-0606 | P12 | config | Record cover.topic as "AI Agents in Production: Architecture, Orchestration & Governance in 2026" | config value equals the canonical article title exactly | todo
T-0607 | P12 | config | Record cover.course "UOH-RL07" and cover.lecturer "Dr. Yoram Segal" in config/setup.json | both string fields present and non-empty | todo
T-0608 | P12 | config | Record cover.author full name(s) of the student(s) in config/setup.json | cover.author present and non-empty string | todo
T-0609 | P12 | config | Record cover.date field or a flag to auto-fill the build date for the cover | cover.date present (ISO string) or cover.auto_date boolean true | todo
T-0610 | P12 | shared | Add a CoverConfig dataclass/loader in src/cosmos77_ex03/shared reading the cover block from config/setup.json | importing CoverConfig and loading returns populated typed fields | todo
T-0611 | P12 | shared | Keep CoverConfig loader file under the 150-line cap and free of hardcoded cover values | scripts/check_line_cap.py passes and no literal "85"/title strings appear in the loader | todo
T-0612 | P12 | cover | Create scripts/generate_cover_pdf.py CLI that renders the cover page to output/cover.pdf | running the script produces output/cover.pdf as a non-empty file | todo
T-0613 | P12 | cover | Make generate_cover_pdf.py read all cover text from config/setup.json via CoverConfig (no hardcoded strings) | grep finds no hardcoded exercise number/score/title literals in the script | todo
T-0614 | P12 | cover | Render the exercise number "3" prominently on the cover PDF | extracted PDF text contains the exercise number token | todo
T-0615 | P12 | cover | Render the self-score "85" on the cover PDF | extracted PDF text contains "85" | todo
T-0616 | P12 | cover | Render the ex03 repository URL on the cover PDF | extracted PDF text contains the github.com ex03 URL | todo
T-0617 | P12 | cover | Render topic, author, course, and lecturer lines on the cover PDF | extracted PDF text contains topic, author, course, and lecturer values | todo
T-0618 | P12 | cover | Render the build/submission date on the cover PDF | extracted PDF text contains the date string | todo
T-0619 | P12 | cover | Add a --output flag to generate_cover_pdf.py defaulting to output/cover.pdf | invoking with --output /tmp/x.pdf writes to that path | todo
T-0620 | P12 | cover | Add a --config flag to generate_cover_pdf.py defaulting to config/setup.json | invoking with a custom config path uses that file | todo
T-0621 | P12 | cover | Keep scripts/generate_cover_pdf.py under the 150-line cap, splitting rendering helpers if needed | scripts/check_line_cap.py reports zero violations | todo
T-0622 | P12 | cover | Ensure generate_cover_pdf.py exits non-zero with a clear message when the config is missing required cover keys | running against a stub config missing keys returns exit code !=0 with an error message | todo
T-0623 | P12 | latex | Decide and document the cover rendering backend (reportlab vs LuaLaTeX template) in a docstring/ADR note | script docstring states the chosen backend and rationale | todo
T-0624 | P12 | tests | Add tests/test_cover_config.py asserting CoverConfig loads exercise_number=3 and self_score=85 from a fixture config | pytest tests/test_cover_config.py passes | todo
T-0625 | P12 | tests | Add a test asserting CoverConfig raises a clear error on missing required keys | test_cover_config_missing_keys passes | todo
T-0626 | P12 | tests | Add tests/test_generate_cover.py that invokes the cover generator with a temp config and asserts output PDF exists and is non-empty | pytest tests/test_generate_cover.py::test_cover_pdf_created passes | todo
T-0627 | P12 | tests | In the cover generator test, extract text from the produced PDF and assert it contains "3", "85", and the ex03 URL | test_cover_pdf_content passes | todo
T-0628 | P12 | tests | Mock any external rendering I/O (no live LaTeX/network) in cover tests to keep them deterministic | tests run offline and pass repeatedly with identical results | todo
T-0629 | P12 | tests | Parametrize cover content assertions over (topic, author, course, lecturer, date) fields | test_cover_pdf_fields[*] all pass | todo
T-0630 | P12 | tests | Assert generate_cover_pdf.py honors the --output flag by writing to a tmp_path target | test_cover_output_flag passes | todo
T-0631 | P12 | qa | Add an output/cover.pdf check to scripts/qa_pdf.py verifying the cover page exists and carries the required tokens | qa_pdf.py reports the cover checks as PASS | todo
T-0632 | P12 | qa | Verify the generated cover.pdf is a single page | qa check asserts cover.pdf page count == 1 | todo
T-0633 | P12 | docs | Document the cover generation step and required config keys in README.md | README.md contains a "Cover PDF" section listing exercise_number, self_score, ex03 URL | todo
T-0634 | P12 | docs | Add the cover-generation command to docs/PLAN.md build sequence | PLAN.md references scripts/generate_cover_pdf.py in the build pipeline | todo
T-0635 | P12 | ci | Wire generate_cover_pdf.py into scripts/build_pdf.sh so the cover is regenerated before/with the main build | build_pdf.sh invokes the cover generator and the run produces output/cover.pdf | todo
T-0636 | P12 | ci | Ensure ruff passes on the new cover script, loader, and tests | ruff check . reports zero findings | todo
T-0637 | P12 | ci | Ensure overall coverage stays >=85% after adding cover code/tests | uv run pytest --cov reports total coverage >=85% | todo
T-0638 | P12 | ci | Commit the cover work as a conventional commit referencing the P12 TODO IDs | git log shows a commit like "feat(cover): ... (P12)" | todo
T-0639 | P12 | docs | Bump or confirm project version remains 1.00 across pyproject/version file ahead of the release | version string reads 1.00 in the canonical version location | todo
T-0640 | P12 | docs | Update docs/TODO.md to mark P12 cover/release tasks and reference their IDs | TODO.md lists the P12 task IDs with statuses | todo
T-0641 | P12 | ci | Create an annotated git tag v1.00 on the release commit | git tag -l v1.00 lists the tag and git show v1.00 displays an annotation message | todo
T-0642 | P12 | ci | Write a release/tag message summarizing HW3 deliverables and acceptance B1-B15 | git show v1.00 message references the HW3 article and key acceptance items | todo
T-0643 | P12 | ci | Push the v1.00 tag to the origin remote | git ls-remote --tags origin lists refs/tags/v1.00 | todo
T-0644 | P12 | ci | Create a GitHub release for tag v1.00 via gh release create | gh release view v1.00 returns the release without error | todo
T-0645 | P12 | ci | Attach the compiled tex/main.pdf and output/cover.pdf as assets on the v1.00 gh release | gh release view v1.00 lists main.pdf and cover.pdf assets | todo
T-0646 | P12 | docs | Write the gh release notes (body) summarizing what is included and how to build | gh release view v1.00 shows non-empty notes mentioning the build command | todo
T-0647 | P12 | docs | Add a docs/RELEASE.md checklist capturing the manual Moodle + collaborator steps for HW3 | docs/RELEASE.md exists and lists Moodle submission and collaborator-invite steps | todo
T-0648 | P12 | docs | In RELEASE.md, record the manual step to add the course collaborator(s) to the GitHub repo | RELEASE.md contains a "Collaborators" section naming the invite action | todo
T-0649 | P12 | docs | In RELEASE.md, record the manual Moodle submission step (upload PDF/repo URL, enter self-score 85) | RELEASE.md "Moodle" section lists the upload and self-score-85 actions | todo
T-0650 | P12 | docs | In RELEASE.md, link the v1.00 release URL and the ex03 repo URL for submission convenience | RELEASE.md contains both the release URL and the ex03 repo URL | todo
T-0651 | P12 | qa | Final phase verification: ruff clean, tests green, coverage >=85%, cover.pdf + main.pdf built, v1.00 tagged and released | a single verification run confirms all five conditions hold | todo
