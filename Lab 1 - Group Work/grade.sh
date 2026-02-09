#!/usr/bin/env bash
set -e

AUTOGRADE_DIR="lab1_files/autograde"
STUDENTS_FILE="$AUTOGRADE_DIR/students.txt"
APPEND_FILE="$AUTOGRADE_DIR/GRADING/APPEND.py"

if [ ! -f "$STUDENTS_FILE" ]; then
  echo "students.txt not found"
  exit 1
fi

if [ ! -f "$APPEND_FILE" ]; then
  echo "APPEND.py not found"
  exit 1
fi

lookup_name() {
  id="$1"
  awk -v id="$id" '
    $1==id {
      last=$NF
      first=""
      for(i=2;i<NF;i++) {
        first = (first ? first" " : "") $i
      }
      print last ", " first
      exit
    }
  ' "$STUDENTS_FILE"
}

for student_dir in "$AUTOGRADE_DIR"/*; do
  [ -d "$student_dir" ] || continue

  id="$(basename "$student_dir")"
  [ "$id" = "GRADING" ] && continue
  [ "$id" = "__MACOSX" ] && continue

  pyfile="$(ls "$student_dir"/*.py 2>/dev/null | head -n 1)"
  [ -n "$pyfile" ] || continue

  outfile="$AUTOGRADE_DIR/dcs211_lab1_${id}.txt"

  cat > "$outfile" <<EOF
==============================
DCS 211: Lab 1
Name: STUDENT_NAME
Score: STUDENT_SCORE
====================================
EOF

  name="$(lookup_name "$id")"
  [ -n "$name" ] || name="UNKNOWN"
  sed -i.bak "s/STUDENT_NAME/$name/" "$outfile" && rm "$outfile.bak"

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
