"""Bindings for the SOAR client."""

import os

import dotenv
from http_client import HttpClient
from utils import consts


dotenv.load_dotenv()

http_client: HttpClient = None


def bind():
    """Binds global variables."""
    global http_client
    http_client = HttpClient(
        os.getenv(consts.ENV_SOAR_URL), os.getenv(consts.ENV_SOAR_APP_KEY)
    )
