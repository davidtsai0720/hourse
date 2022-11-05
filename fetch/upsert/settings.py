from enum import Enum


class Settings(Enum):

    headers = {'content-type': 'application/json; charset=utf-8'}
    URL = 'http://localhost:8080/hourse'
    status_code = 204
