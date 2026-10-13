#!/usr/bin/env sh
cd "$(dirname "$0")"
if [ ! -d .venv ]; then
  echo "First run: setting up, this takes about a minute..."
  python3 -m venv .venv && .venv/bin/pip install -q -r requirements.txt || exit 1
fi
[ -f .env ] || { echo "No .env file yet. Rename .env.example to .env and paste your token (README step 3)."; exit 1; }
.venv/bin/python bot.py
