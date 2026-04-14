#!/usr/bin/env bash
set -euo pipefail

echo "Starting App"
streamlit run --server.port=8080 streamlit_app.py
