#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="${1:-lab1_files/file_renaming/reorganized}"

export LC_TIME=C
TODAY="$(date +'%d%b%Y')" 

make_filename() {
  local chapter="$1"
  local dataset="$2"
  echo "CH${chapter}_DS${dataset}_${TODAY}.sav"
}

shopt -s nullglob

for chapter_dir in "$ROOT_DIR"/Chapter*; do
  [[ -d "$chapter_dir" ]] || continue

  chapter_num="${chapter_dir##*/Chapter}"

  for file in "$chapter_dir"/DataSet*.sav; do
    base="$(basename "$file")"

    dataset_num="$(echo "$base" | sed -E 's/^DataSet([0-9]+)\.sav$/\1/')"
    [[ "$dataset_num" =~ ^[0-9]+$ ]] || continue

    new_name="$(make_filename "$chapter_num" "$dataset_num")"
    mv -f "$file" "$chapter_dir/$new_name"
  done
done

echo "Rename complete."
