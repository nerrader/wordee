#!/usr/bin/env bash
set -e

uv run nuitka \
  --mode=app \
  --macos-app-icon=assets/wordee-icon.icns \
  --enable-plugin=pyside6 \
  --output-filename=wordee \
  --output-dir=dist \
  src/wordee/main.py
