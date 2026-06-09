#!/usr/bin/env bash
# scripts/build_pdf.sh — compile tex/main.pdf via the 4-pass pipeline:
#   lualatex --interaction=nonstopmode main.tex
#   biber main
#   lualatex --interaction=nonstopmode main.tex   (x2 — resolves TOC + citations)
# Native LuaLaTeX (MacTeX/TeX Live) is the default path. Set USE_DOCKER_LATEX=1
# to compile in the texlive/texlive Docker image instead (for a grader without
# a local TeX install).
set -uo pipefail

HERE="$(cd "$(dirname "$0")/.." && pwd)"
TEX_DIR="${1:-$HERE/tex}"
cd "$TEX_DIR" || { echo "ERROR: no tex dir at $TEX_DIR" >&2; exit 1; }
rm -f main.pdf

compile_native() {
  lualatex --interaction=nonstopmode main.tex || true
  biber main || true
  lualatex --interaction=nonstopmode main.tex || true
  lualatex --interaction=nonstopmode main.tex || true
}

compile_docker() {
  docker run --rm -v "$TEX_DIR":/work -w /work texlive/texlive:latest sh -c \
    'lualatex --interaction=nonstopmode main.tex; biber main; \
     lualatex --interaction=nonstopmode main.tex; \
     lualatex --interaction=nonstopmode main.tex'
}

if command -v lualatex >/dev/null 2>&1 && command -v biber >/dev/null 2>&1; then
  compile_native
elif [ "${USE_DOCKER_LATEX:-0}" = "1" ] && command -v docker >/dev/null 2>&1; then
  compile_docker
else
  echo "ERROR: lualatex/biber not found." >&2
  echo "  Install MacTeX:  brew install --cask mactex-no-gui" >&2
  echo "  then:            eval \"\$(/usr/libexec/path_helper)\"" >&2
  echo "  or re-run with:  USE_DOCKER_LATEX=1 (requires Docker)" >&2
  exit 2
fi

if [ -f main.pdf ]; then
  echo "OK: $TEX_DIR/main.pdf built"
else
  echo "ERROR: main.pdf was not produced (see main.log)" >&2
  exit 1
fi
