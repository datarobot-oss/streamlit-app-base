#!/usr/bin/env bash
echo "Starting App"

export token="$DATAROBOT_API_TOKEN"
export endpoint="$DATAROBOT_ENDPOINT"
export app_base_url_path="$STREAMLIT_SERVER_BASE_URL_PATH"

streamlit run --server.port=8080 streamlit_app.py