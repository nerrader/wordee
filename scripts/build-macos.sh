#!/usr/bin/env bash
set -e

uv run nuitka \
  --mode=app-dist \
  --macos-app-icon=assets/wordee-icon.icns \
  src/wordee/main.py

mv dist/main.app dist/WORDEE-x86_64.app

# apparently its supposed to zip apps
ditto -c -k --sequesterRsrc --keepParent \
  "dist/WORDEE-x86_64.app" \
  "dist/WORDEE-x86_64.app.zip"
