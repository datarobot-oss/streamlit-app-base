# Streamlit app base template

An empty Streamlit application base template to kickstart custom application development.
The DataRobot client is pre-configured and uses the application owner's API key automatically.
The template includes example tabs that fetch and display live data from the DataRobot API
(version info, projects, deployments, use cases) to give you a concrete starting point.

## Setup

### Running locally

Install dependencies with [uv](https://docs.astral.sh/uv/):

```shell
cd src
uv sync
```

Set the required environment variables:

```shell
export DATAROBOT_API_TOKEN="<your API token>"   # Developer Tools page in DataRobot
export DATAROBOT_ENDPOINT="https://app.datarobot.com/api/v2"
```

Then start the app:

```shell
uv run streamlit run streamlit_app.py
```

### Running as a Custom Application

Custom applications can be created via the NextGen Registry's **Applications** page or
with [DRApps](https://github.com/datarobot/dr-apps/blob/main/README.md).

When running as a Custom Application, `DATAROBOT_API_TOKEN` and `DATAROBOT_ENDPOINT` are
injected by the platform automatically — no manual configuration needed.

## Making DataRobot API calls

`utils.py` provides a `_get(path)` helper that makes authenticated GET requests using the
token and endpoint stored in Streamlit session state. Use it to call any DataRobot API endpoint:

```python
from utils import _get

projects = _get("/projects/")
deployments = _get("/deployments/")
```

For calls that should be cached across reruns (e.g. user info), use `@st.cache_data`:

```python
@st.cache_data(show_spinner=False)
def get_my_data(token: str, endpoint: str) -> dict | None:
    return _get("/my-endpoint/")
```

Pass `st.session_state.token` and `st.session_state.endpoint` as arguments so the cache
invalidates automatically if the credentials change.

## Add runtime parameters

Runtime parameters let you configure the app from the DataRobot UI without changing code.
A commented-out example is provided in `metadata.yaml.sample`. To activate it:

**Step 1** — Copy `metadata.yaml.sample` to `metadata.yaml` 

**Step 2** — Uncomment the block in `metadata.yaml` and set your parameter name.

**Step 3** — Add the corresponding field to `Config` in `config.py`:

```python
class Config(DataRobotAppFrameworkBaseSettings):
    deployment_id: str = ""
```

`DataRobotAppFrameworkBaseSettings` reads the `MLOPS_RUNTIME_PARAM_DEPLOYMENT_ID` env var
that the platform injects and exposes it as `Config().deployment_id` — no shell script
exports needed.

**Step 3** — Use it in your app:

```python
from config import Config

config = Config()
deployment_id = config.deployment_id
```

## LLM Gateway

The **LLM Gateway** tab shows all models available to your DataRobot account and lets you
send a single-turn chat message. Model discovery uses `datarobot.genai.LLMGatewayCatalog`;
chat goes through [LiteLLM](https://github.com/BerriAI/litellm) with the `datarobot/` model prefix.

For a full multi-turn chat application with streaming, citations, and deployment support,
see the [QA App Streamlit](https://github.com/datarobot-oss/qa-app-streamlit) template.

## Health check

Streamlit exposes a built-in health endpoint at `/_stcore/health`. The DataRobot platform
uses this automatically — no custom implementation needed.

## Streamlit configuration file

This template includes a `config.toml` in `src/.streamlit/` with sensible defaults.
Adjust it to your preferences ([read more](https://docs.streamlit.io/develop/concepts/configuration/theming)):

```toml
[browser]
gatherUsageStats = false            # Disables component usage tracking by Streamlit

[theme]
base="dark"
primaryColor="#297ab4"              # Accent color of user interaction elements (button, checkbox, etc.)
backgroundColor="#0e1117"           # Background for the main content area
secondaryBackgroundColor="#22272b"  # Background for sidebar and various interactive widgets

[client]
toolbarMode = "minimal"             # Hides the Streamlit actions from the toolbar
```
