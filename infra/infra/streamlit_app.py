"""
Deploy Streamlit application to DataRobot as a Custom Application.

Supports both new deployment and replacing an existing application
via the DATAROBOT_APPLICATION_ID environment variable.
"""

import os
import re
from pathlib import Path
from typing import Final

import pulumi
import pulumi_datarobot
from datarobot_pulumi_utils.schema.apps import ApplicationSourceArgs
from datarobot_pulumi_utils.schema.apps import CustomAppResourceBundles
from datarobot_pulumi_utils.schema.exec_envs import RuntimeEnvironments
from datarobot_pulumi_utils.pulumi.stack import PROJECT_NAME

from . import project_dir, use_case


EXCLUDE_PATTERNS = [
    re.compile(pattern)
    for pattern in [
        r".*tests/.*",
        r".*\.coverage",
        r".*\.DS_Store",
        r".*\.pyc",
        r".*\.ruff_cache/.*",
        r".*\.venv/.*",
        r".*\.mypy_cache/.*",
        r".*__pycache__/.*",
        r".*\.pytest_cache/.*",
        r".*htmlcov/.*",
        r".*\.data/.*",
        r".*\.env",
    ]
]

__all__ = [
    "streamlit_app",
    "streamlit_app_source",
]

# Path to the Streamlit application source
streamlit_application_path = project_dir.parent / "src"

# Runtime parameter definitions
DATAROBOT_API_TOKEN: Final[str] = "DATAROBOT_API_TOKEN"
DATAROBOT_ENDPOINT: Final[str] = "DATAROBOT_ENDPOINT"

streamlit_app_runtime_parameters: list[
    pulumi_datarobot.ApplicationSourceRuntimeParameterValueArgs
] = [
    pulumi_datarobot.ApplicationSourceRuntimeParameterValueArgs(
        type="credential",
        key=DATAROBOT_API_TOKEN,
        value=os.environ.get(DATAROBOT_API_TOKEN, ""),
    ),
    pulumi_datarobot.ApplicationSourceRuntimeParameterValueArgs(
        type="string",
        key=DATAROBOT_ENDPOINT,
        value=os.environ.get(DATAROBOT_ENDPOINT, "https://app.datarobot.com/api/v2"),
    ),
]


def get_streamlit_app_files() -> list[tuple[str, str]]:
    """Collect all application files from src/ for deployment."""
    source_files = []
    for dirpath, dirnames, filenames in os.walk(
        streamlit_application_path, followlinks=True
    ):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(file_path, streamlit_application_path)
            rel_path = rel_path.replace(os.path.sep, "/")
            source_files.append((os.path.abspath(file_path), rel_path))

    source_files = [
        (file_path, file_name)
        for file_path, file_name in source_files
        if not any(
            exclude_pattern.match(file_name) for exclude_pattern in EXCLUDE_PATTERNS
        )
    ]
    return source_files


# --- Pulumi resources ---

streamlit_app_resource_name: str = f"Streamlit App Base [{PROJECT_NAME}]"

streamlit_app_source_args = ApplicationSourceArgs(
    resource_name=streamlit_app_resource_name,
    base_environment_id=RuntimeEnvironments.PYTHON_312_APPLICATION_BASE.value.id,
).model_dump(mode="json", exclude_none=True)

streamlit_app_source = pulumi_datarobot.ApplicationSource(
    files=get_streamlit_app_files(),
    runtime_parameter_values=streamlit_app_runtime_parameters,
    resources=pulumi_datarobot.ApplicationSourceResourcesArgs(
        resource_label=CustomAppResourceBundles.CPU_XL.value.id,
    ),
    **streamlit_app_source_args,
)

# Support replacing an existing application
existing_app_id = os.environ.get("DATAROBOT_APPLICATION_ID", "")

if existing_app_id:
    pulumi.info(
        f"Replacing existing application '{existing_app_id}' with new source"
    )
    streamlit_app = pulumi_datarobot.CustomApplication.get(
        resource_name=f"{streamlit_app_resource_name} [EXISTING]",
        id=existing_app_id,
    )
    # Update the existing application's source version
    streamlit_app = pulumi_datarobot.CustomApplication(
        resource_name=streamlit_app_resource_name,
        source_version_id=streamlit_app_source.version_id,
        use_case_ids=[use_case.id],
        allow_auto_stopping=True,
        resources=pulumi_datarobot.CustomApplicationResourcesArgs(
            resource_label=CustomAppResourceBundles.CPU_XL.value.id,
        ),
        opts=pulumi.ResourceOptions(
            depends_on=[streamlit_app_source],
            import_=existing_app_id,
        ),
    )
else:
    streamlit_app = pulumi_datarobot.CustomApplication(
        resource_name=streamlit_app_resource_name,
        source_version_id=streamlit_app_source.version_id,
        use_case_ids=[use_case.id],
        allow_auto_stopping=True,
        resources=pulumi_datarobot.CustomApplicationResourcesArgs(
            resource_label=CustomAppResourceBundles.CPU_XL.value.id,
        ),
        opts=pulumi.ResourceOptions(depends_on=[streamlit_app_source]),
    )

pulumi.export("DATAROBOT_APPLICATION_ID", streamlit_app.id)
pulumi.export(
    f"{streamlit_app_resource_name} URL",
    streamlit_app.application_url,
)
