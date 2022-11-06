# -*- coding: utf-8 -*-
from enum import Enum
import os

HOST = os.getenv('SERVICE_HOST')
PORT = os.getenv('SERVICE_PORT')


class Settings(Enum):

    headers = {'content-type': 'application/json; charset=utf-8'}
    URL = f'http://{HOST}:{PORT}/api/hourse'
    status_code = 204
