#!/usr/bin/env bash

BASE_DIR="$HOME/dcs211_exam"

cd "$BASE_DIR"/data

mv notes.txt lab_notes.txt

mv "$BASE_DIR"/data/lab3.py "$BASE_DIR"/backup/lab3.py

cp "$BASE_DIR"/data/lab1.py "$BASE_DIR"/scripts/lab1.py

rm "$BASE_DIR"/data/lab2.py