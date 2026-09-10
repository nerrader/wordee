#!/usr/bin/env bash
set -e

uv run nuitka \
  --mode=app-dist \
  --macos-app-icon=assets/wordee-icon.icns \
  src/wordee/main.py

mv dist/main.app dist/WORDEE-x86_64.app
