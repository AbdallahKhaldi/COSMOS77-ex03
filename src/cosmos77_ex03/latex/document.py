"""Build ``tex/main.tex``: cover, TOC, chapter inputs, visuals, bibliography.

Covers B2 (cover sheet), B3 (TOC + chapter division), and interleaves the B4
diagram, B5 figures, B6 table, and B7 formula at sensible points so all appear
in the compiled PDF.
"""

from __future__ import annotations

_SPECIALS = {"&": r"\&", "%": r"\%", "_": r"\_", "#": r"\#", "$": r"\$"}


def _esc(text: object) -> str:
    return "".join(_SPECIALS.get(ch, ch) for ch in str(text))


def _titlepage(article: dict) -> str:
    return (
        "\\begin{titlepage}\\centering\n"
        f"  {{\\LARGE {_esc(article.get('title', 'Untitled'))}\\par}}\\vspace{{2cm}}\n"
        f"  {{\\large {_esc(article.get('author', ''))}\\par}}\\vspace{{1cm}}\n"
        f"  {{{_esc(article.get('course', ''))}\\par}}\n"
        f"  {{{_esc(article.get('instructor', ''))}\\par}}{{\\today\\par}}\n"
        "\\end{titlepage}\n"
    )


def _figure(pdf: str, caption: str, label: str) -> str:
    return (
        "\\begin{figure}[htbp]\\centering\n"
        f"  \\includegraphics[width=0.8\\linewidth]{{figures/{pdf}}}\n"
        f"  \\caption{{{caption}}}\\label{{{label}}}\n"
        "\\end{figure}\n"
    )


def build_main_tex(article: dict, chapter_indices: list[int]) -> str:
    """Assemble main.tex, inputting each section with visuals interleaved."""
    n = len(chapter_indices)
    mid = min(7, n)
    out = [
        "\\input{preamble.tex}",
        "\\begin{document}",
        _titlepage(article),
        "\\tableofcontents\\newpage",
        "",
    ]
    for pos, idx in enumerate(chapter_indices, start=1):
        out.append(f"\\input{{sections/ch_{idx:02d}.tex}}")
        if pos == 1:
            out.append("\\input{diagram.tex}")
            out.append(
                _figure(
                    "adoption.pdf",
                    "Enterprise AI-agent adoption, 2023--2026 (projected).",
                    "fig:adoption",
                )
            )
        if pos == mid:
            out.append("\\input{table.tex}")
            out.append(_figure("frameworks.pdf", "Agent framework production-fit, 2026.", "fig:fw"))
        if pos == n:
            out.append("\\input{formula.tex}")
    out += ["", "\\printbibliography", "\\end{document}", ""]
    return "\n".join(out)
