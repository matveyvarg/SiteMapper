import os
import importlib
import logging

import bottle

# READ .env file
from sitemap.exceptions import EnvNotSet
from dotenv import load_dotenv, find_dotenv

load_dotenv(dotenv_path=find_dotenv())

# DETERMINE CONFIG
config = os.getenv('CONFIG', 'local')

# LOAD CONFIG
settings_module = importlib.import_module(f".{config}", "sitemap.settings")
configuration: dict = getattr(settings_module, "configuration")
logger: logging.Logger = getattr(settings_module, "logger", logging.getLogger(__name__))

# DEFINE BASE_DIR
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


def _setup_configuration() -> dict:
    """
    Check if all env vars are setted and add template path
    :return:
    """
    REQUIRED_ENVS = [
        'host',
        'port'
    ]

    for key in REQUIRED_ENVS:
        if not configuration.get(key):
            raise EnvNotSet(key)

    templates_path = configuration.get("TEMPLATE_PATHS", [
        os.path.abspath(os.path.join(BASE_DIR, 'views'))
    ])
    for index, template_path in enumerate(templates_path):
        bottle.TEMPLATE_PATH.insert(index, template_path)

    return configuration


settings = _setup_configuration()
