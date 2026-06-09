"""Deterministic Markdown -> LuaLaTeX conversion for chapter sections (B11).

Converts a chapter's Markdown (headings, paragraphs, lists, bold/italic/code,
inline ``\\cite{...}``) into a clean LaTeX fragment. The Hebrew BiDi chapter is
wrapped in ``\\selectlanguage{hebrew}`` so babel(bidi=basic) lays it out RTL with
inline English handled automatically (B8).
"""

from __future__ import annotations

import re

_SPECIALS = {
    "\\": r"\textbackslash{}",
    "{": r"\{",
    "}": r"\}",
    "&": r"\&",
    "%": r"\%",
    "$": r"\$",
    "#": r"\#",
    "_": r"\_",
    "~": r"\textasciitilde{}",
    "^": r"\textasciicircum{}",
}
_CITE_RE = re.compile(r"\\cite\{[^}]*\}")
_FENCE_RE = re.compile(r"^```.*$", re.MULTILINE)


def _escape(text: str) -> str:
    return "".join(_SPECIALS.get(ch, ch) for ch in text)


def _inline(text: str) -> str:
    """Escape LaTeX specials, then apply inline Markdown, preserving ``\\cite``."""
    cites: list[str] = []

    def _stash(match: re.Match) -> str:
        cites.append(match.group(0))
        return f"\x00{len(cites) - 1}\x00"

    text = _CITE_RE.sub(_stash, text)
    text = _escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"\\textbf{\1}", text)
    text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"\\textit{\1}", text)
    text = re.sub(r"`(.+?)`", r"\\texttt{\1}", text)
    return re.sub(r"\x00(\d+)\x00", lambda m: cites[int(m.group(1))], text)


def _heading(line: str) -> str | None:
    for marker, cmd in (("### ", "subsection"), ("## ", "section"), ("# ", "section")):
        if line.startswith(marker):
            return f"\\{cmd}{{{_inline(line[len(marker) :].strip())}}}"
    return None


def _list_block(lines: list[str], pattern: str, env: str) -> str:
    items = "\n".join("  \\item " + _inline(re.sub(pattern, "", ln)) for ln in lines)
    return f"\\begin{{{env}}}\n{items}\n\\end{{{env}}}"


def _block_to_tex(block: str) -> str:
    lines = [ln for ln in block.splitlines() if ln.strip()]
    if not lines:
        return ""
    if all(re.match(r"^\s*[-*]\s+", ln) for ln in lines):
        return _list_block(lines, r"^\s*[-*]\s+", "itemize")
    if all(re.match(r"^\s*\d+\.\s+", ln) for ln in lines):
        return _list_block(lines, r"^\s*\d+\.\s+", "enumerate")
    head = _heading(lines[0])
    parts: list[str] = []
    if head:
        parts.append(head)
        lines = lines[1:]
    if lines:
        parts.append(_inline(" ".join(lines)))
    return "\n\n".join(parts)


def md_to_latex(markdown: str, *, hebrew: bool = False) -> str:
    """Convert chapter Markdown to a LaTeX fragment (Hebrew wrapped for BiDi)."""
    text = _FENCE_RE.sub("", markdown).strip()
    blocks = re.split(r"\n\s*\n", text)
    body = "\n\n".join(b for b in (_block_to_tex(bl) for bl in blocks) if b)
    if hebrew:
        return f"\\selectlanguage{{hebrew}}\n{body}\n\\selectlanguage{{english}}\n"
    return body + "\n"
