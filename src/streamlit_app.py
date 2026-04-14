import streamlit as st
from datarobot import Client
from datarobot.client import set_client

from constants import *
from utils import (
    get_current_user,
    get_deployments,
    get_llm_models,
    get_projects,
    get_use_cases,
    get_version,
    initiate_session_state,
    llm_chat,
)

# Basic application page configuration, modify values in `constants.py`
st.set_page_config(
    page_title=I18N_APP_NAME,
    page_icon=APP_FAVICON,
    layout=APP_LAYOUT,
    initial_sidebar_state=SIDEBAR_DEFAULT_STATE,
)


def start_streamlit():
    # Setup DR client — reads DATAROBOT_API_TOKEN and DATAROBOT_ENDPOINT automatically.
    # If credentials are missing or invalid the app shows an actionable error instead of
    # crashing with a stack trace.
    try:
        dr = Client()
    except Exception as exc:
        st.error(
            "Could not connect to DataRobot. "
            "Make sure **DATAROBOT_API_TOKEN** and **DATAROBOT_ENDPOINT** are set correctly.\n\n"
            f"`{exc}`"
        )
        st.stop()

    set_client(dr)
    initiate_session_state(dr)

    token = st.session_state.token
    endpoint = st.session_state.endpoint

    with st.sidebar:
        st.logo(APP_LOGO)

        user = get_current_user(token, endpoint)
        if user:
            st.write(f"**{user.get('username', '')}**")
            st.caption(user.get('email', ''))
            st.success("Connected", icon="✅")
        else:
            st.error("DataRobot unreachable", icon="🔴")

        st.divider()
        st.caption("Resources")
        st.markdown(
            "[📖 App Templates]"
            "(https://docs.datarobot.com/en/docs/wb-apps/app-templates/index.html)"
        )
        st.markdown(
            "[⚙️ Custom App API Reference]"
            "(https://docs.datarobot.com/en/docs/api/reference/public-api/custom_applications.html)"
        )
        if st.session_state.apidocs_url:
            st.markdown(
                f"[🔌 DataRobot API Docs]({st.session_state.apidocs_url})"
            )

    st.header(I18N_APP_NAME)
    if I18N_APP_DESCRIPTION:
        st.write(I18N_APP_DESCRIPTION)

    # -----------------------------------------------------------------------
    # Example: fetch and display DataRobot data.
    # Replace or extend these tabs with your own application logic.
    # -----------------------------------------------------------------------
    tab_version, tab_projects, tab_deployments, tab_use_cases, tab_llm = st.tabs(
        ["API Version", "My Projects", "My Deployments", "My Use Cases", "LLM Gateway"]
    )

    with tab_version:
        data = get_version()
        if data:
            st.json(data)

    with tab_projects:
        data = get_projects()
        if data:
            st.json(data)

    with tab_deployments:
        data = get_deployments()
        if data:
            st.json(data)

    with tab_use_cases:
        data = get_use_cases()
        if data:
            st.json(data)

    with tab_llm:
        st.markdown(
            "Send a message to any model available in the DataRobot LLM Gateway.\n\n"
            "For a more advanced chat interface check out the [Q&A App Streamlit](https://github.com/datarobot-oss/qa-app-streamlit) template."
        )

        models = get_llm_models(token, endpoint)
        if not models:
            st.info(
                "No LLM Gateway models found. "
                "Check that your DataRobot account has LLM Gateway access."
            )
        else:
            model = st.selectbox("Model", options=list(models))
            prompt = st.text_area("Message", placeholder="Ask something…")
            if st.button("Send", disabled=not prompt):
                with st.spinner("Thinking…"):
                    response = llm_chat(
                        model,
                        [{"role": "user", "content": prompt}],
                        token,
                        endpoint,
                    )
                if response:
                    st.markdown(response)


if __name__ == "__main__":
    start_streamlit()
