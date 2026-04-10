import logging
from urllib.parse import urlparse

import requests
import streamlit as st
from datarobot import Client

logger = logging.getLogger(__name__)


def initiate_session_state(dr: Client) -> None:
    if "token" not in st.session_state:
        st.session_state.token = dr.token
    if "endpoint" not in st.session_state:
        st.session_state.endpoint = dr.endpoint
    if "apidocs_url" not in st.session_state:
        parsed = urlparse(dr.endpoint.rstrip("/"))
        st.session_state.apidocs_url = (
            f"{parsed.scheme}://{parsed.netloc}/apidocs/" if parsed.netloc else None
        )


def _get(path: str) -> dict | list | None:
    """Make an authenticated GET request to the DataRobot API."""
    token = st.session_state.token
    endpoint = st.session_state.endpoint
    try:
        resp = requests.get(
            f"{endpoint.rstrip('/')}/{path.lstrip('/')}",
            headers={"Authorization": f"Bearer {token}"},
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()
    except requests.HTTPError as exc:
        logger.error("DataRobot API error for %s: %s", path, exc)
        st.error(f"DataRobot API error: {exc}")
    except Exception as exc:
        logger.exception("Request failed for %s", path)
        st.error(f"Request failed: {exc}")
    return None


@st.cache_data(show_spinner=False)
def get_current_user(token: str, endpoint: str) -> dict | None:
    """Fetch the authenticated user's account info (/account/info/)."""
    try:
        resp = requests.get(
            f"{endpoint.rstrip('/')}/account/info/",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()
    except Exception:
        logger.exception("Failed to fetch current user")
        return None


def get_version() -> dict | None:
    """Fetch the DataRobot platform version (/version/)."""
    return _get("/version/")


def get_projects() -> dict | None:
    """Fetch the list of projects (/projects/)."""
    return _get("/projects/")


def get_deployments() -> dict | None:
    """Fetch the list of deployments (/deployments/)."""
    return _get("/deployments/")


def get_use_cases() -> dict | None:
    """Fetch the list of use cases (/useCases/)."""
    return _get("/useCases/")


@st.cache_data(show_spinner=False)
def get_llm_models(token: str, endpoint: str) -> list[str]:
    """List model names available in the DataRobot LLM Gateway (/genai/llmgw/catalog/)."""
    try:
        resp = requests.get(
            f"{endpoint.rstrip('/')}/genai/llmgw/catalog/",
            headers={"Authorization": f"Bearer {token}"},
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json().get("data", [])
        return [item["model"] for item in data]
    except Exception:
        logger.exception("Failed to fetch LLM Gateway models")
        return []


def llm_chat(model: str, messages: list[dict], token: str, endpoint: str) -> str | None:
    """Send a chat request to the DataRobot LLM Gateway via LiteLLM.

    LiteLLM routes to DataRobot when the model name carries a "datarobot/" prefix.
    Model names returned by get_llm_models() are accepted as-is.
    """
    import litellm

    try:
        if not model.startswith("datarobot/"):
            model = f"datarobot/{model}"
        response = litellm.completion(
            model=model,
            messages=messages,
            api_key=token,
            api_base=endpoint,
        )
        return response.choices[0].message.content
    except Exception as exc:
        logger.exception("LLM Gateway chat failed")
        st.error(f"LLM Gateway error: {exc}")
        return None
