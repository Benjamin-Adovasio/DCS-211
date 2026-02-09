#!/usr/bin/env bash
set -euo pipefail

SRC_DIR="${1:-lab1_files/file_renaming/Salkind 6e Data Sets}"
DEST_DIR="${2:-lab1_files/file_renaming/reorganized}"

mkdir -p "$DEST_DIR"

shopt -s nullglob

for f in "$SRC_DIR"/Chapter\ *\ Data\ Set\ *.sav; do
  base="$(basename "$f")"  # e.g., "Chapter 12 Data Set 3.sav"

  # Extract chapter number k and dataset number j robustly.
  # Expected format: Chapter k Data Set j.sav
  k="$(printf '%s' "$base" | sed -E 's/^Chapter ([0-9]+) Data Set ([0-9]+)\.sav$/\1/')"
  j="$(printf '%s' "$base" | sed -E 's/^Chapter ([0-9]+) Data Set ([0-9]+)\.sav$/\2/')"

  # If the file doesn't match the pattern, skip it (e.g., "Sample Data Set.sav")
  if [[ "$k" == "$base" || "$j" == "$base" ]]; then
    continue
  fi

  chap_dir="$DEST_DIR/Chapter${k}"
  mkdir -p "$chap_dir"

  cp -f "$f" "$chap_dir/DataSet${j}.sav"
done

echo "Done. Created reorganized structure at: $DEST_DIR"
