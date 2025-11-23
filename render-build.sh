#!/usr/bin/env bash
set -o errexit

pip install --upgrade pip setuptools wheel
pip install -r requirements.txt --use-deprecated=legacy-resolver

uvicorn app.main:app --host 0.0.0.0 --port 10000

