# Streamlit app base template

## What's in this repository?
In this repository you will find an empty Streamlit application base template to kickstart your custom app development.

The Datarobot client is already set up for you to use, it uses the Application owners' API token by default. 

## How do I set it up?
You can run the app in DataRobot via Custom Applications or run the Streamlit app directly.
Custom Applications can be created either via the registry workshop or
using [DRApps](https://github.com/datarobot/dr-apps/blob/main/README.md)

Make sure to define the required variables for the app to talk to DataRobot. If you run the app from local or another
environment than DataRobots Custom Applications you'll need to set the env variables. When this app is run via
custom applications workshop they should be set automatically.

```shell
#start-app.sh
export token="$DATAROBOT_API_TOKEN"  # Your API token from DR developer tools page
export endpoint="$DATAROBOT_ENDPOINT"  # Example: https://app.datarobot.com/api/v2/
```

## How to add and use runtime parameters?
Create a metadata.yaml file in your application source folder. Here is an example of a DEPLOYMENT_ID which will create
an environment variable called `MLOPS_RUNTIME_PARAM_DEPLOYMENT_ID`:
```yaml
runtimeParameterDefinitions:
- fieldName: DEPLOYMENT_ID
  type: string
```

Once this file is part of your Application source in DataRobot, it will display the new runtime parameter(s) as part of the
app configuration.

To use the parameters we recommend to add them via `start-app.sh`, add this conditional export before `gunicorn` starts:
```shell
if [ -n "$MLOPS_RUNTIME_PARAM_DEPLOYMENT_ID" ]; then
  export deployment_id="$MLOPS_RUNTIME_PARAM_DEPLOYMENT_ID"
fi
```

Now you can use `os.getenv("deployment_id")` within your application code.
We suggest to add every new env variable to the `initiate_session_state` function, that way they can be used across the
app with ease.

## Streamlit config file
This base template comes with a `config.toml` file in the `src/.streamlit` directory. You can adjust your app preferences
in this file. There are some preset defaults:
Read more on https://docs.streamlit.io/develop/concepts/configuration/theming

```toml
[browser]
gatherUsageStats = false            # This disables the component usage tracking by Streamlit

[theme]
base="dark" 
primaryColor="#297ab4"              # Accent color of user interaction elements (button, checkbox, etc
backgroundColor="#0e1117"           # Background for the main content area
secondaryBackgroundColor="#22272b"  # Background for sidebar and various interactive widgets

[client]
toolbarMode = "minimal"             # Hides the Streamlit actions from the toolbar (clear cache, rerun, custom themes)
```
