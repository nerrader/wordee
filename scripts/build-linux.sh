#!/usr/bin/env bash
set -e

uv run nuitka \
  --mode=app \
  --enable-plugin=pyside6 \
  --product-name=WORDEE \
  --linux-create-installer \
  --linux-app-icon=assets/wordee-icon.png \
  --output-filename=wordee \
  --output-dir=dist \
  src/wordee/main.py
