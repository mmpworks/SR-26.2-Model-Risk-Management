#!/usr/bin/env bash
# render-pdf.sh: render the submission package and the current spec draft to PDF.
#
# Usage (from submission/build/):
#   ./render-pdf.sh all                  # every document below
#   ./render-pdf.sh <name> [<name> ...]  # e.g. proposal spec
#
# Names: cover-letter, executive-summary, proposal, control-overlay,
#        handbook-mapping, test-vectors-summary, spec.
# Output goes to submission/artifacts/<name>.pdf (git-ignored).
#
# Reproducibility: SOURCE_DATE_EPOCH is pinned to the last commit's timestamp,
# so the same commit renders the same PDF bytes on the same toolchain
# (pandoc + XeLaTeX + DejaVu fonts, as installed by render-pdf.yml).
set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SUB="$(cd "$HERE/.." && pwd)"
ROOT="$(cd "$SUB/.." && pwd)"
OUT="$SUB/artifacts"
mkdir -p "$OUT"

if [ -z "${SOURCE_DATE_EPOCH:-}" ]; then
  SOURCE_DATE_EPOCH="$(git -C "$ROOT" log -1 --format=%ct 2>/dev/null || date +%s)"
fi
export SOURCE_DATE_EPOCH
export FORCE_SOURCE_DATE=1  # XeTeX/xdvipdfmx honor SOURCE_DATE_EPOCH only with this set

# The newest spec draft by version number (chain-of-custody-DRAFT-X.Y.Z.md).
latest_spec() {
  ls "$ROOT"/spec/chain-of-custody-DRAFT-*.md | sort -V | tail -n 1
}

source_for() {
  case "$1" in
    cover-letter)         echo "$SUB/cover-letter.md" ;;
    executive-summary)    echo "$SUB/executive-summary.md" ;;
    proposal)             echo "$SUB/proposal.md" ;;
    control-overlay)      echo "$SUB/appendices/control-overlay.md" ;;
    handbook-mapping)     echo "$SUB/appendices/handbook-mapping.md" ;;
    test-vectors-summary) echo "$SUB/appendices/test-vectors-summary.md" ;;
    spec)                 latest_spec ;;
    *) echo "render-pdf.sh: unknown document '$1'" >&2; return 2 ;;
  esac
}

ALL=(cover-letter executive-summary proposal control-overlay handbook-mapping test-vectors-summary spec)

render() {
  local name="$1" src
  local -a extra=()
  src="$(source_for "$name")"
  if [ "$name" = spec ]; then extra+=(--toc); fi
  # Pin the PDF trailer /ID to the source bytes. Otherwise xdvipdfmx derives it
  # from pandoc's random temp directory and every run differs.
  local id
  id="$(sha256sum "$src" | cut -c1-32)"
  extra+=(-V "header-includes=\\special{pdf:trailerid [<$id><$id>]}")
  echo "rendering $name <- ${src#"$ROOT"/}"
  # --resource-path lets relative links and images resolve from the source's folder.
  pandoc "$src" \
    --from=gfm+tex_math_dollars \
    --pdf-engine=xelatex \
    --resource-path="$(dirname "$src")" \
    "${extra[@]}" \
    -V mainfont="DejaVu Serif" \
    -V sansfont="DejaVu Sans" \
    -V monofont="DejaVu Sans Mono" \
    -V geometry:margin=1in \
    -V colorlinks=true \
    -V linkcolor=blue \
    -V urlcolor=blue \
    -o "$OUT/$name.pdf"
}

if [ "$#" -eq 0 ]; then
  sed -n '2,12p' "$0"; exit 2
fi
if [ "$1" = all ]; then set -- "${ALL[@]}"; fi
for name in "$@"; do render "$name"; done
echo "done: $(ls "$OUT"/*.pdf | wc -l) PDF(s) in ${OUT#"$ROOT"/}"
