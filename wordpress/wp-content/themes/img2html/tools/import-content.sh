#!/usr/bin/env bash
set -e
THEME_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
mkdir -p "$THEME_DIR/tools/blocks"
exit 0
