#!/usr/bin/env bash
set -e

uv run nuitka \
  --mode=app \
  --linux-create-installer \
  --linux-app-icon=assets/wordee-icon.png \
  src/wordee/main.py
