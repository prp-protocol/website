#!/usr/bin/env sh

set -eu

if [ "$(git branch --show-current)" != "main" ]; then
  echo "error: GitHub publication must run from the main branch" >&2
  exit 1
fi

if [ -n "$(git status --short)" ]; then
  echo "error: commit or discard local changes before publishing" >&2
  exit 1
fi

if [ "$(git remote get-url github)" != "git@github.com:prp-protocol/website.git" ]; then
  echo "error: the github remote is missing or points to an unexpected repository" >&2
  exit 1
fi

git push github main:main main:gh-pages
