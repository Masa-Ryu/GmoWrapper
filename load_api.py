import json


def load_config(file_name="gmo_key.json"):
    """
    load api key and secret from gmo_keys.json
    format:

    {
    "api_key": "your_api_key",
    "api_secret": "your_api_secret"
    }

    """
    with open(file_name, "r") as f:
        config = json.load(f)
        api_key = config["api_key"]
        api_secret = config["api_secret"]
    return api_key, api_secret
