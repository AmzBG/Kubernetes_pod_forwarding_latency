#!/usr/bin/env bash
set -euo pipefail

# Tunable parallelism: use CONCURRENCY=N ./build_pods.sh to override
CONCURRENCY="${CONCURRENCY:-$(command -v nproc >/dev/null 2>&1 && nproc || echo 4)}"

echo "==> Using concurrency: ${CONCURRENCY}"
command -v docker >/dev/null 2>&1 || { echo "Docker not found in PATH"; exit 1; }

# find all dirs named pod<number> at repo root
mapfile -t POD_DIRS < <(find . -maxdepth 1 -mindepth 1 -type d -regex './pod[0-9]+' | sort -V)
if [[ ${#POD_DIRS[@]} -eq 0 ]]; then
  echo "No pod<number> directories found at repo root."
  exit 1
fi

build_one() {
  local dir="$1"
  local base="${dir#./}"            # e.g., pod3
  local tag="$base"                 # tag: pod3
  local dockerfile="$dir/Dockerfile"

  if [[ ! -f "$dockerfile" ]]; then
    echo "[SKIP] $dir -> no Dockerfile"
    return 0
  fi

  echo "[BUILD] $dir -> tag: $tag"
  docker build -t "$tag" "$dir"
  echo "[DONE ] $dir"
}

# Run builds in background, limited by CONCURRENCY
pids=()
for d in "${POD_DIRS[@]}"; do
  # throttle jobs
  while (( $(jobs -r | wc -l) >= CONCURRENCY )); do
    sleep 0.2
  done

  build_one "$d" &
  pids+=("$!")
done

# wait for all
fail=0
for pid in "${pids[@]}"; do
  if ! wait "$pid"; then
    fail=1
  fi
done

if (( fail )); then
  echo "One or more builds failed."
  exit 1
fi

echo "All builds completed successfully."
