#!/usr/bin/env bash
# Build the presentation deck PDF from docs/report/slides.md using Marp.
#
# Marp renders via a Chromium engine. This script reuses the Chromium that
# Playwright already installed for the project (no extra download). Run from
# anywhere:  bash docs/report/build_slides.sh
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
ROOT="$(cd "$HERE/../.." && pwd)"
OUT="$HERE/pdf"
mkdir -p "$OUT"

SRC="$HERE/slides.md"
TMP="$(mktemp -t atc_slides).md"
# Strip the team-internal "_Draft ..._" disclaimer line for the final deck.
grep -v '^_Draft' "$SRC" > "$TMP"

# Locate a Chromium engine: prefer Playwright's, fall back to a system Chrome.
CHROME=""
if [ -x "$ROOT/.venv/bin/python" ]; then
  CHROME="$("$ROOT/.venv/bin/python" -c 'from playwright.sync_api import sync_playwright; p=sync_playwright().start(); print(p.chromium.executable_path); p.stop()' 2>/dev/null || true)"
fi
if [ -z "$CHROME" ] && [ -x "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" ]; then
  CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
fi

echo "Using Chromium: ${CHROME:-<marp default>}"
CHROME_PATH="$CHROME" npx -y @marp-team/marp-cli@latest "$TMP" \
  --pdf --allow-local-files \
  -o "$OUT/ATC_Readback_Verifier_Slides.pdf"

echo "Wrote $OUT/ATC_Readback_Verifier_Slides.pdf"
