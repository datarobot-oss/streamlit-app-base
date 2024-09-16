import streamlit as st
from datarobot import Client
from datarobot.client import set_client

from constants import *

# Basic application page configuration, modify values in `constants.py`
st.set_page_config(page_title=I18N_APP_NAME, page_icon=APP_FAVICON, layout=APP_LAYOUT,
                   initial_sidebar_state=SIDEBAR_DEFAULT_STATE)


def start_streamlit():

    # Setup DR client
    set_client(Client(token=st.session_state.token, endpoint=st.session_state.endpoint))

    st.logo(APP_LOGO)
    st.header('Hello world')


if __name__ == "__main__":
    start_streamlit()
