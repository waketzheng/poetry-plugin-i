#!/usr/bin/env bash

set -e
set -x

[ -f ../pyproject.toml ] && cd ..
poetry run pytest tests/
