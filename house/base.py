# -*- coding: utf-8 -*-
import abc

from selenium import webdriver


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
    def run(self) -> None:
        pass
