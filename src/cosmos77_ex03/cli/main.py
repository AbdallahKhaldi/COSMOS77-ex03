"""Command-line entry point for `cosmos77-article`.

A thin dispatcher over the SDK. Each subcommand (smoke, research, write, figures,
assemble, build, qa, run) is wired to the SDK in its phase; until then it prints
guidance instead of crashing.
"""

from __future__ import annotations

import argparse
import sys

_COMMANDS = ("smoke", "research", "write", "figures", "assemble", "build", "qa", "run")


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

    args = build_parser().parse_args(argv)
    if args.version:
        print(f"cosmos77-article {__version__}")
        return 0
    if args.command is None:
        build_parser().print_help()
        return 0
    return _dispatch(args.command)


def _dispatch(command: str) -> int:
    """Run one pipeline stage via the SDK and print a short summary."""
    from cosmos77_ex03.sdk.sdk import SDK

    sdk = SDK()
    if command == "smoke":
        print(f"reply: {sdk.smoke()}")
        print(f"token_usage: {sdk.spec_sheet()}")
        return 0
    if command == "research":
        outline = sdk.research()
        print(f"research: {len(outline.chapters)} chapters, {len(outline.citations)} citations")
        print(f"token_usage: {sdk.spec_sheet()}")
        return 0
    print(f"`{command}` is not wired yet — it lands in its phase.")
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
