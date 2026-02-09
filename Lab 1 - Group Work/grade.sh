#!/usr/bin/env bash
set -euo pipefail

AUTOGRADE_DIR="${1:-lab1_files/autograde}"
STUDENTS_FILE="$AUTOGRADE_DIR/students.txt"
APPEND_FILE="$AUTOGRADE_DIR/GRADING/APPEND.py"

[[ -f "$STUDENTS_FILE" ]] || { echo "students.txt missing"; exit 1; }
[[ -f "$APPEND_FILE" ]] || { echo "APPEND.py missing"; exit 1; }

mapfile -t IDS < <(
  find "$AUTOGRADE_DIR" -mindepth 1 -maxdepth 1 -type d \
  ! -name GRADING ! -name "__MACOSX" -printf '%f\n' | sort
)

lookup_name() {
  local id="$1"
  awk -v id="$id" '
    $1==id {
      last=$NF
      first=""
      for(i=2;i<NF;i++) first=(first ? first" " : "")$i
      print last", "first
    }
  ' "$STUDENTS_FILE"
}

for id in "${IDS[@]}"; do
  student_dir="$AUTOGRADE_DIR/$id"
  pyfile="$(find "$student_dir" -maxdepth 1 -name '*.py' | head -n 1 || true)"
  [[ -n "$pyfile" ]] || continue

  outfile="$AUTOGRADE_DIR/dcs211_lab1_${id}.txt"

  cat > "$outfile" <<EOF
==============================
DCS 211: Lab 1
Name: STUDENT_NAME
Score: STUDENT_SCORE
====================================
EOF

  name="$(lookup_name "$id")"
  sed -i.bak "s/STUDENT_NAME/${name:-UNKNOWN}/" "$outfile" && rm "$outfile.bak"

  graded="$student_dir/__graded_${id}.py"
  cp "$pyfile" "$graded"

  sed -i.bak -E 's/^([[:space:]]*)print/\1# print/' "$graded"
  sed -i.bak -E 's/^([[:space:]]*)main[[:space:]]*\(/\1# main(/' "$graded"
  rm "$graded.bak"

  cat "$APPEND_FILE" >> "$graded"

  set +e
  output="$(python3 "$graded" 2>&1)"
  set -e

  {
    echo
    echo "---- AUTOGRADE OUTPUT ----"
    echo "$output"
    echo "---- END AUTOGRADE OUTPUT ----"
  } >> "$outfile"

  score="$(echo "$output" | tail -n 1 | grep -Eo '[0-9]+[[:space:]]*/[[:space:]]*[0-9]+' || echo N/A)"
  sed -i.bak "s/STUDENT_SCORE/$score/" "$outfile" && rm "$outfile.bak"

  echo "Graded $id"
done

echo "Grading complete."
