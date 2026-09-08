#!/usr/bin/env bash
set -e

uv run nuitka \
  --standalone \
  --enable-plugin=pyside6 \
  --linux-create-installer \
  --linux-app-icon=assets/wordee-icon.png \
  --output-filename=wordee \
  --output-dir=dist \
  src/wordee/main.py
