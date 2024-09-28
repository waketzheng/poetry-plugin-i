#!/bin/sh -e
set -x

[ -f ../pyproject.toml ] && cd ..
ruff format .
ruff check --fix .
