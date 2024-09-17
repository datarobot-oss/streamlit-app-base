import os

import streamlit as st


def initiate_session_state():
    # Env variables
    if 'token' not in st.session_state:
        st.session_state.token = os.getenv("token")
    if 'endpoint' not in st.session_state:
        st.session_state.endpoint = os.getenv("endpoint")
