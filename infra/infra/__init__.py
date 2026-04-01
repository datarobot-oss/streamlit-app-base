"""
Core Pulumi resources for Streamlit App Base.
"""

import os
from pathlib import Path

from datarobot_pulumi_utils.pulumi.stack import PROJECT_NAME
import pulumi
import pulumi_datarobot as datarobot

__all__ = ["use_case", "project_dir"]

project_dir = Path(__file__).parent.parent

if use_case_id := os.environ.get("DATAROBOT_DEFAULT_USE_CASE"):
    pulumi.info(f"Using existing use case '{use_case_id}'")
    use_case = datarobot.UseCase.get(
        id=use_case_id,
        resource_name="Streamlit App Base [PRE-EXISTING]",
    )
else:
    use_case = datarobot.UseCase(
        resource_name=f"Streamlit App Base [{PROJECT_NAME}]",
        description="Streamlit App Base - DataRobot Custom Application",
    )
