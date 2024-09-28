#!/usr/bin/env bash

set -e
set -x

[ -f ../pyproject.toml ] && cd ..
ruff check --extend-select=I .
ruff format --check .
mypy .
echo Done. ✨ 🍰 ✨
