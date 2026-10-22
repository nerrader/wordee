#!/usr/bin/env bash
set -e

rm -rf dist

uv run --with "Nuitka[app] @ git+https://github.com/Nuitka/Nuitka.git@factory" \
  -- nuitka \
  --mode=app-dist \
  --macos-app-icon=assets/wordee-icon.icns \
  src/wordee/main.py

mv dist/main.app dist/WORDEE-macos-arm64.app

# apparently its supposed to zip apps
ditto -c -k --sequesterRsrc --keepParent \
  "dist/WORDEE-macos-arm64.app" \
  "dist/WORDEE-macos-arm64.app.zip"
