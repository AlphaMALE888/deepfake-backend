#!/usr/bin/env bash
# Fix pip and install manually
pip install --upgrade pip setuptools wheel

# install dependencies safely
pip install -r requirements.txt --use-deprecated=legacy-resolver

# Run the app
uvicorn app.main:app --host 0.0.0.0 --port 10000
