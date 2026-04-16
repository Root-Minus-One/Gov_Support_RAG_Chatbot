import os
import yaml
from dotenv import load_dotenv

def get_api_key(PROVIDED_KEY):
    "load api key from environment"

    api_key = os.getenv(PROVIDED_KEY)

    if not api_key:
        raise KeyError(f"API KEY not found for {PROVIDED_KEY}")

    return api_key 


def load_config():
    "find and load configuration yaml file"

    config_path = "../config/config.yaml"

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Config file not found: {config_path}")
    
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}



