#!/usr/bin/env bash
set -euo pipefail

CONCURRENCY="${CONCURRENCY:-$(nproc 2>/dev/null || echo 4)}"

find . -maxdepth 1 -mindepth 1 -type d -regex './pod[0-9]+' \
| sort -V \
| xargs -I{} -P"$CONCURRENCY" bash -c '
  [ -f "{}/Dockerfile" ] || { echo "[SKIP] {}"; exit 0; }
  tag="$(basename "{}")"
  echo "[BUILD] {} -> $tag"
  docker build -t "$tag" "{}"
'