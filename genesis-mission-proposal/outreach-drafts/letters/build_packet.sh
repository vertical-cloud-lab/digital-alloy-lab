#!/usr/bin/env bash
# Assemble Valimet subaward packet into a single PDF using pandoc + xelatex.
# Run from outreach-drafts/letters/ directory.
set -euo pipefail
cd "$(dirname "$0")"

ORDER=(
  00-cover-letter.md
  00a-EXECUTIVE-SUMMARY-AND-CHECKLIST.md
  README.md
  WALKTHROUGH.md
  FAQ.md
  01-valimet-loc-prefilled.md
  02-valimet-scope-of-work.md
  03-valimet-cost-share-guide.md
  04-valimet-cost-share-worksheet.md
  05-valimet-budget-justification.md
  06-valimet-tfc-guide.md
  07-valimet-coi-reps.md
  08-valimet-data-ip.md
  09-valimet-key-personnel-request.md
  10-valimet-facilities-request.md
  11-valimet-byu-osp-mechanics.md
)

# Concatenate with page breaks between sections.
TMP=$(mktemp --suffix=.md)
trap "rm -f $TMP" EXIT

cat > "$TMP" <<'HDR'
---
title: "FLAIME — Valimet Subaward Outreach Packet"
subtitle: "DE-FOA-0003612, Topic 3-B — Brigham Young University Prime"
author: "Sterling G. Baird, PI"
date: "April 2026"
geometry: margin=1in
fontsize: 11pt
colorlinks: true
toc: true
toc-depth: 1
---

HDR

for f in "${ORDER[@]}"; do
  echo -e "\n\n\\\\newpage\n\n" >> "$TMP"
  cat "$f" >> "$TMP"
done

pandoc "$TMP" \
  --pdf-engine=xelatex \
  -V mainfont="DejaVu Serif" \
  -V monofont="DejaVu Sans Mono" \
  -V sansfont="DejaVu Sans" \
  -o valimet-subaward-packet.pdf

echo "Built: $(pwd)/valimet-subaward-packet.pdf ($(stat -c%s valimet-subaward-packet.pdf) bytes)"
