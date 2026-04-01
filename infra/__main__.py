"""
Discover and load all Pulumi resource modules in the infra directory.
Output exported variables to a configuration file for local development.
"""

from infra import *  # noqa: F403
import importlib
from pathlib import Path
from os import getenv

from datarobot_pulumi_utils.pulumi import default_collector, finalize

DEFAULT_EXPORT_PATH: Path = Path(
    getenv(
        "PULUMI_EXPORT_PATH", str(Path(__file__).parent.parent / "pulumi_config.json")
    )
)
INFRA_DIR = Path(__file__).parent / "infra"


def import_infra_modules():
    """Dynamically import all top-level modules in the infra package."""
    for file_path in INFRA_DIR.glob("*.py"):
        filename = file_path.name
        if filename in ("__init__.py", "__main__.py"):
            continue

        module_name = f"infra.{filename[:-3]}"
        module = importlib.import_module(module_name)

        for attr in dir(module):
            if attr.startswith("_"):
                continue
            globals()[attr] = getattr(module, attr)


# Import all modules
import_infra_modules()

# Export outputs to JSON for local development
default_collector.output_path = DEFAULT_EXPORT_PATH
finalize()
