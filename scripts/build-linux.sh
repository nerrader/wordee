#!/usr/bin/env bash
set -e

uv run nuitka \
  --mode=app-dist \
  --linux-create-installer \
  --linux-app-icon=assets/wordee-icon.png \
  src/wordee/main.py

mv dist/main.AppImage dist/WORDEE.AppImage
