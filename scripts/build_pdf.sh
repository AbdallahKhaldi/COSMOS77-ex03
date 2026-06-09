#!/usr/bin/env bash
# scripts/build_pdf.sh — compile the LaTeX project in tex/ to tex/main.pdf.
#
# PLACEHOLDER (Phase 0). Phase 9 fills this with the real four-pass pipeline:
#   lualatex --interaction=nonstopmode main.tex
#   biber main
#   lualatex --interaction=nonstopmode main.tex
#   lualatex --interaction=nonstopmode main.tex
# and exits non-zero on a fatal LaTeX error.
set -euo pipefail

echo "build_pdf.sh is a Phase-0 placeholder; the compile pipeline lands in Phase 9."
exit 0
