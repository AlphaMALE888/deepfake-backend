#!/usr/bin/env bash
set -o errexit  # stop script on error

# Upgrade pip, wheel, setuptools
pip install --upgrade pip setuptools wheel

# Install dependencies safely
pip install -r requirements.txt --use-deprecated=legacy-resolver || exit 1

# Start the app
uvicorn app.main:app --host 0.0.0.0 --port 10000
