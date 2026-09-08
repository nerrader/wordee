#!/usr/bin/env bash
set -e

uv run nuitka \
  --mode=app \
  --macos-app-icon=assets/wordee-icon.icns \
  src/wordee/main.py
