#!/bin/sh
# Build the copper/DED technical proposal in a DAL checkout and overwrite
# Baird_ONR_YIP_ProjectDescription_LATEST.pdf next to this script, so a viewer
# that watches that one file (SumatraPDF, VS Code) redraws after every build.
#
#   sh build_latest.sh [DAL_DIR] [--sync-tex] [--snapshot TAG]
#
# DAL_DIR       a vertical-cloud-lab/digital-alloy-lab checkout or worktree
#               (default: $DAL_DIR). It must hold figures-cu-ded/ for the .tex.
# --sync-tex    copy this folder's .tex into DAL before building; without it,
#               DAL's own .tex is built.
# --snapshot T  also keep a dated copy, Baird_ONR_YIP_ProjectDescription_DRAFT_T.pdf,
#               for a build that is sent somewhere (Kuali, SPO, a DAL drop).
# --submit      build without the red TODO markers and the TODO list, into
#               Baird_ONR_YIP_ProjectDescription_SUBMIT.pdf; LATEST is left alone.
set -eu

HERE=$(cd "$(dirname "$0")" && pwd)
TEX=onr-yip-technical-proposal-cu-ded
LATEST="$HERE/Baird_ONR_YIP_ProjectDescription_LATEST.pdf"
SYNC=0
TAG=
SUBMIT=0
DAL=${DAL_DIR:-}

while [ $# -gt 0 ]; do
  case "$1" in
    --sync-tex) SYNC=1 ;;
    --snapshot) TAG=$2; shift ;;
    --submit) SUBMIT=1 ;;
    *) DAL=$1 ;;
  esac
  shift
done
[ -n "$DAL" ] || { echo "usage: sh build_latest.sh DAL_DIR [--sync-tex] [--snapshot TAG]" >&2; exit 2; }
SRC="$DAL/near-term-submissions/onr-yip"
[ -f "$SRC/$TEX.tex" ] || { echo "no $TEX.tex in $SRC" >&2; exit 2; }

if [ "$SYNC" = 1 ]; then
  cp "$HERE/$TEX.tex" "$SRC/$TEX.tex"
  echo "copied this folder's .tex into $SRC"
fi

cd "$SRC"
# the red TODO markers print no text; their notes go to an uncounted list at the end
[ -f make_todo_list.py ] && python make_todo_list.py "$TEX.tex"
JOB=$TEX
INPUT="$TEX.tex"
if [ "$SUBMIT" = 1 ]; then
  JOB=$TEX-submit
  INPUT="\def\submissionbuild{}\input{$TEX.tex}"
  LATEST="$HERE/Baird_ONR_YIP_ProjectDescription_SUBMIT.pdf"
fi
for pass in 1 2 3; do
  if ! xelatex -interaction=nonstopmode -halt-on-error -jobname="$JOB" "$INPUT" > "${TMPDIR:-/tmp}/$JOB.build.txt" 2>&1; then
    tail -30 "${TMPDIR:-/tmp}/$JOB.build.txt" >&2
    echo "xelatex failed on pass $pass; $(basename "$LATEST") left as it was" >&2
    exit 1
  fi
done

pages=$(pdfinfo "$JOB.pdf" | awk '/^Pages:/ {print $2}')
overfull=$(grep -c 'Overfull \\hbox' "$JOB.log" || true)
undefined=$(grep -c -E 'Reference .* undefined|Citation .* undefined' "$JOB.log" || true)
echo "pages: $pages  overfull lines: $overfull  undefined references: $undefined"

# Write beside the target, then rename, so a watching viewer never reads a half-written file.
cp "$JOB.pdf" "$LATEST.tmp"
mv -f "$LATEST.tmp" "$LATEST"
echo "wrote $LATEST"
[ "$JOB" = "$TEX" ] || rm -f "$JOB".aux "$JOB".log "$JOB".out "$JOB".toc "$JOB".pdf

if [ -n "$TAG" ]; then
  cp "$LATEST" "$HERE/Baird_ONR_YIP_ProjectDescription_DRAFT_$TAG.pdf"
  echo "wrote snapshot Baird_ONR_YIP_ProjectDescription_DRAFT_$TAG.pdf"
fi
