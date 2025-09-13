#!/bin/bash
set -euo pipefail

# --- Functions ---
slugify() {
  # lowercase, spaces -> hyphens, keep only a-z0-9- and underscores
  echo "$1" \
    | tr '[:upper:]' '[:lower:]' \
    | sed -E 's/[[:space:]]+/-/g; s/[^a-z0-9_-]+/-/g; s/-+/-/g; s/^-|-$//g'
}

next_number_in_dir() {
  local dir="$1"
  # Find the highest NN in files like lesson-NN-YYYY-MM-DD.ipynb
  local last_num
  last_num=$(
    ls "$dir"/lesson-*-*.ipynb 2>/dev/null \
      | sed -E 's#.*/lesson-([0-9]+)-.*#\1#' \
      | sort -n \
      | tail -1
  )
  if [[ -z "${last_num:-}" ]]; then
    printf "%02d" 1
  else
    printf "%02d" $((10#$last_num + 1))
  fi
}

ensure_template() {
  if [[ ! -f "template.ipynb" ]]; then
    cat > template.ipynb <<'JSON'
{
 "cells": [
  {"cell_type":"markdown","metadata":{},"source":["# 🚀 LLM Lesson\n\nShort description of this lesson.\n"]},
  {"cell_type":"code","metadata":{},"source":["# Setup\n","import os, sys\n","sys.path.append(os.getcwd())\n","from openai import OpenAI\n","client = OpenAI(base_url=\"http://localhost:11434/v1\", api_key=\"ollama\")\n","print(\"✅ Client ready\")\n"]},
  {"cell_type":"code","metadata":{},"source":["# Quick test\n","r = client.chat.completions.create(model=\"llama3.2:3b\", messages=[{\"role\":\"user\",\"content\":\"Say hi in one line.\"}])\n","print(r.choices[0].message.content)\n"]},
  {"cell_type":"markdown","metadata":{},"source":["## 📝 Notes\n","- Key points:\n","- Questions:\n"]}
 ],
 "metadata": {
  "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
  "language_info": {"name": "python", "version": "3"}
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
JSON
    echo "ℹ️  Created a minimal template.ipynb (since none existed)."
  fi
}

# --- Main ---
cd "$(dirname "$0")"

# 1) Ask for prefix
read -rp "Enter lesson prefix (e.g., 'embeddings', 'rag', 'qa-tests'): " PREFIX
if [[ -z "${PREFIX// }" ]]; then
  echo "❌ Prefix cannot be empty."
  exit 1
fi

# 2) Slugify and make/use directory
SLUG=$(slugify "$PREFIX")
DIR="$SLUG"
mkdir -p "$DIR"

# 3) Work out next number + date
NN=$(next_number_in_dir "$DIR")
TODAY=$(date +%Y-%m-%d)
FILENAME="$DIR/lesson-$NN-$TODAY.ipynb"

# 4) Ensure template exists, then copy
ensure_template
cp template.ipynb "$FILENAME"

echo "✅ Created $FILENAME"
echo "   Folder: $DIR"