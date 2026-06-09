"""The §13.1 PDF QA checklist validator (B1-B9, B15).

Reads the compiled ``tex/`` project (preamble, main.tex, sections, main.pdf/.bbl/
.log/.out) and asserts the technical-wrapper requirements the professor checks.
Returns structured results; critical failures gate the build.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

_HEBREW = re.compile(r"[֐-׿]")


@dataclass
class Check:
    """One checklist item: a name, pass/fail, whether it is build-gating, a detail."""

    name: str
    ok: bool
    critical: bool
    detail: str = ""


def page_count(pdf_path: Path) -> int:
    """Return the PDF page count via pdfplumber (0 if missing/unreadable)."""
    try:
        import pdfplumber

        with pdfplumber.open(str(pdf_path)) as pdf:
            return len(pdf.pages)
    except Exception:
        return 0


def _read_tex(tex_dir: Path) -> str:
    parts: list[str] = []
    for name in ("preamble.tex", "main.tex"):
        path = tex_dir / name
        if path.exists():
            parts.append(path.read_text(encoding="utf-8"))
    sections = tex_dir / "sections"
    if sections.is_dir():
        parts += [f.read_text(encoding="utf-8") for f in sorted(sections.glob("*.tex"))]
    return "\n".join(parts)


def _hebrew_section(tex_dir: Path) -> tuple[bool, str]:
    sections = tex_dir / "sections"
    for f in sorted(sections.glob("*.tex")) if sections.is_dir() else []:
        text = f.read_text(encoding="utf-8")
        switched = "selectlanguage{hebrew}" in text or "foreignlanguage{hebrew}" in text
        if switched and _HEBREW.search(text):
            return True, f.name
    return False, "no Hebrew section with a babel language switch"


def run_checks(tex_dir: Path | str, target_pages: int = 15, tol: int = 3) -> list[Check]:
    """Run the §13.1 checklist over the compiled project; return results."""
    d = Path(tex_dir)
    tex = _read_tex(d)
    pdf, bbl, log = d / "main.pdf", d / "main.bbl", d / "main.log"
    pages = page_count(pdf) if pdf.exists() else 0
    bbl_text = bbl.read_text(encoding="utf-8") if bbl.exists() else ""
    log_text = log.read_text(encoding="utf-8", errors="ignore") if log.exists() else ""
    overfull = len(re.findall(r"Overfull \\hbox", log_text))
    figs = list((d / "figures").glob("*.pdf")) if (d / "figures").is_dir() else []
    heb_ok, heb_detail = _hebrew_section(d)
    return [
        Check("B11 main.pdf exists", pdf.exists(), True, str(pdf)),
        Check("B1 ~15 pages", pages >= target_pages - tol, True, f"{pages} pages"),
        Check("B4/B5 includegraphics", "\\includegraphics" in tex, True),
        Check("B5 figure PDFs present", len(figs) >= 1, True, f"{len(figs)} pdf(s)"),
        Check("B6 non-overflow table", "tabularx" in tex or "\\begin{table}" in tex, True),
        Check("B6 no overfull hbox", overfull == 0, False, f"{overfull} overfull hbox"),
        Check("B7 display formula", bool(re.search(r"\\begin\{(equation|align)", tex)), True),
        Check("B3 table of contents", "\\tableofcontents" in tex, True),
        Check("B3 headers/footers", "\\fancyhead" in tex or "\\fancyfoot" in tex, True),
        Check("B8 Hebrew BiDi chapter", heb_ok, True, heb_detail),
        Check("B9 citations + .bbl", "\\cite" in tex and len(bbl_text.strip()) > 0, True),
        Check("B9 clickable refs (.out)", (d / "main.out").exists(), False),
    ]


def has_critical_failure(checks: list[Check]) -> bool:
    """True if any build-gating check failed."""
    return any(c.critical and not c.ok for c in checks)


def format_report(checks: list[Check]) -> str:
    """Render a human-readable §13.1 checklist report."""
    lines = ["PDF QA — §13.1 technical checklist", "=" * 36]
    for c in checks:
        tag = "PASS" if c.ok else ("FAIL" if c.critical else "WARN")
        lines.append(f"[{tag}] {c.name}" + (f" — {c.detail}" if c.detail else ""))
    failed = [c for c in checks if c.critical and not c.ok]
    lines.append("=" * 36)
    lines.append("ALL CRITICAL CHECKS PASS" if not failed else f"{len(failed)} CRITICAL FAILURE(S)")
    return "\n".join(lines)
