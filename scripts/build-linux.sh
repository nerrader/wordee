#!/usr/bin/env bash
set -e

uv run nuitka \
  --mode=app \
  --linux-app-icon=assets/wordee-icon.png \
  src/wordee/main.py
