import json
import logging

import requests

from .settings import Settings
from .tools import DecimalEncoder


def upsert(data: dict) -> None:
    resp = requests.post(
        Settings.URL.value,
        headers=Settings.headers.value,
        data=json.dumps(data, cls=DecimalEncoder))
    assert resp.status_code == Settings.status_code.value, f'response: {resp.json()}, body: {data}'
