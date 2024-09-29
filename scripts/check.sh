#!/usr/bin/env bash

set -e
set -x

[ -f ../pyproject.toml ] && cd ..
poetry run ruff check --extend-select=I .
poetry run ruff format --check .
poetry run mypy .
echo Done. ✨ 🍰 ✨
