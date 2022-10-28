# -*- coding: utf-8 -*-
from selenium import webdriver


class Base:

    def __init__(self, driver: webdriver.Firefox) -> None:
        self.driver = driver

    def run(self) -> None:
        pass

    def url_parse(self, url: str) -> dict:
        obj = url.split('?')
        if len(obj) != 2:
            return {}
        result = {}
        for row in obj[1].split('&'):
            key, value = row.split('=')
            result[key] = value
        return result
