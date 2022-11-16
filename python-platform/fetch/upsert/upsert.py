# -*- coding: utf-8 -*-
import json

import requests

from .settings import Settings
from .tools import DecimalEncoder


def handle_upsert_hourse(data: dict) -> str:
    body = json.dumps(data, cls=DecimalEncoder, ensure_ascii=False).encode("utf-8")
    resp = requests.put(
        url=Settings.URL.value, data=body,
        headers=Settings.headers.value,
    )
    if resp.status_code != Settings.status_code.value:
        raise ValueError(f"response: {resp.json()}, body: {data}")
