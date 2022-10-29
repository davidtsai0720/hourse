# -*- coding: utf-8 -*-
from collections import namedtuple
import abc
import json
import os

from selenium import webdriver

Node = namedtuple('Node', ('tag', 'class_name'))


class URL:

    @staticmethod
    def parse_params(url: str) -> dict:
        obj = url.split('?')
        if len(obj) != 2:
            return {}
        result = {}
        for row in obj[1].split('&'):
            k, v = row.split('=')
            result[k] = v
        return result

    @staticmethod
    def build(host: str, params: dict) -> str:
        args = '&'.join(f'{k}={v}' for k, v in params.items())
        return f'{host}?{args}'


class House(abc.ABC):

    def __init__(self, driver: webdriver.Firefox) -> None:
        self.driver = driver

    @abc.abstractmethod
    def run(self, param: any) -> None:
        pass

    @property
    def wdir(self) -> str:
        try:
            return self._wdir
        except AttributeError:
            wd = os.getcwd()
            wdir = os.path.join(wd, 'output')
            if not os.path.exists(wdir):
                os.mkdir(wdir)
            self._wdir = wdir
            return self._wdir

    def save(self, dest: str, data: list) -> None:
        path = os.path.join(self.wdir, dest)
        with open(path, 'w') as f:
            f.write(json.dumps(data))
