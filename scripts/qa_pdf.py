"""CLI wrapper: run the §13.1 PDF QA checklist on the tex/ project (Phase 9).

Usage: ``uv run python scripts/qa_pdf.py [tex_dir]``. Exits non-zero if any
critical check fails. The checklist logic lives in ``cosmos77_ex03.latex.qa``.
"""

from __future__ import annotations

import sys
from pathlib import Path

from cosmos77_ex03.latex.qa import format_report, has_critical_failure, run_checks


def main(argv: list[str] | None = None) -> int:
    """Run the checklist and print the report; return a process exit code."""
    args = argv if argv is not None else sys.argv[1:]
    tex_dir = Path(args[0]) if args else Path("tex")
    checks = run_checks(tex_dir)
    print(format_report(checks))
    return 1 if has_critical_failure(checks) else 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
