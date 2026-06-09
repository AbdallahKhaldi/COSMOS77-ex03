"""Command-line entry point for `cosmos77-article`.

Phase 0 ships a minimal dispatcher; each subcommand (smoke, research, write,
figures, assemble, build, qa, run) is wired to the SDK in its own phase. Until
then, naming a not-yet-wired command prints guidance instead of crashing.
"""

from __future__ import annotations

import argparse
import sys

_COMMANDS = (
    "smoke",
    "research",
    "write",
    "figures",
    "assemble",
    "build",
    "qa",
    "run",
)


def build_parser() -> argparse.ArgumentParser:
    """Construct the top-level argument parser."""
    parser = argparse.ArgumentParser(
        prog="cosmos77-article",
        description="CrewAI + LaTeX generator for the UOH-RL07 HW3 article.",
    )
    parser.add_argument("command", nargs="?", choices=_COMMANDS, help="pipeline stage to run")
    parser.add_argument("--version", action="store_true", help="print the version and exit")
    return parser


def main(argv: list[str] | None = None) -> int:
    """Parse arguments and dispatch. Returns a process exit code."""
    from cosmos77_ex03 import __version__

    parser = build_parser()
    args = parser.parse_args(argv)
    if args.version:
        print(f"cosmos77-article {__version__}")
        return 0
    if args.command is None:
        parser.print_help()
        return 0
    if args.command == "smoke":
        return _cmd_smoke()
    print(
        f"`{args.command}` is not wired yet — it lands in its phase. "
        "See ../CLAUDE_CODE_PLAYBOOK.md for the build order."
    )
    return 0


def _cmd_smoke() -> int:
    """Run the live Gemini smoke crew and print the reply + token usage."""
    from cosmos77_ex03.sdk.sdk import SDK

    sdk = SDK()
    reply = sdk.smoke()
    print(f"reply: {reply}")
    print(f"token_usage: {sdk.gatekeeper.spec_sheet(provider=sdk.config.active_provider())}")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
