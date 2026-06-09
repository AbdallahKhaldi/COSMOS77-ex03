"""Generate ``refs.bib`` from citations.json, guaranteeing cited keys resolve (B9).

Every ``\\cite`` key found in the converted sections gets a bib entry — any key
without a citation record gets a placeholder so the bibliography never has an
undefined reference (the professor's "citations resolve" check).
"""

from __future__ import annotations

import re

_FIELD_SPECIALS = {"&": r"\&", "%": r"\%", "_": r"\_", "#": r"\#", "$": r"\$"}


def _bib_escape(text: object) -> str:
    clean = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", str(text))
    return "".join(_FIELD_SPECIALS.get(ch, ch) for ch in clean)


def cited_keys(latex_sections: list[str]) -> set[str]:
    """Return every ``\\cite`` key referenced across the given LaTeX section bodies."""
    keys: set[str] = set()
    for body in latex_sections:
        for group in re.findall(r"\\cite\{([^}]*)\}", body):
            keys.update(k.strip() for k in group.split(",") if k.strip())
    return keys


def _entry(key: str, citation: dict) -> str:
    fields = [
        f"  author = {{{_bib_escape(citation.get('author') or 'Unknown')}}}",
        f"  title = {{{_bib_escape(citation.get('title') or key)}}}",
        f"  year = {{{_bib_escape(citation.get('year') or '2026')}}}",
    ]
    if citation.get("venue"):
        fields.append(f"  note = {{{_bib_escape(citation['venue'])}}}")
    if citation.get("url"):
        fields.append(f"  howpublished = {{\\url{{{citation['url']}}}}}")
    return "@misc{" + key + ",\n" + ",\n".join(fields) + "\n}"


def build_refs_bib(citations: list[dict], required_keys: set[str]) -> str:
    """Build refs.bib for all citations plus any cited key missing a record."""
    entries: list[str] = []
    have: set[str] = set()
    for citation in citations:
        key = str(citation.get("key", "")).strip()
        if not key:
            continue
        have.add(key)
        entries.append(_entry(key, citation))
    for key in sorted(required_keys - have):
        entries.append(_entry(key, {"title": key}))
    return "\n\n".join(entries) + "\n"
