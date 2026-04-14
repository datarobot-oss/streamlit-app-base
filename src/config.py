from datarobot.core.config import DataRobotAppFrameworkBaseSettings


class Config(DataRobotAppFrameworkBaseSettings):
    # Declare your runtime parameters here — each field maps to an entry in metadata.yaml.
    # DataRobotAppFrameworkBaseSettings reads them from the MLOPS_RUNTIME_PARAM_* env vars
    # that the platform injects automatically, so no manual exports in start-app.sh are needed.
    #
    # Example — add a deployment ID runtime parameter:
    #   deployment_id: str = ""
    #
    # Then add the corresponding entry to metadata.yaml:
    #   runtimeParameterDefinitions:
    #   - fieldName: DEPLOYMENT_ID
    #     type: string
    pass
