# -*- coding: utf-8 -*-
from collections import namedtuple
from collections.abc import Iterator
import abc
import json
import os
import random
import logging
import time

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup


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


class AbcParam(abc.ABC):

    @abc.abstractmethod
    def __init__(self, param: dict) -> None:
        pass

    @abc.abstractmethod
    def dict(self) -> dict:
        return {}

    @abc.abstractmethod
    def alive(self) -> bool:
        return False

    @abc.abstractmethod
    def can_update_total_count(self) -> bool:
        return False

    def set_next(self) -> None:
        self.page += 1

    def set_total_count(self, num: int) -> None:
        self.total_count = num


class House(abc.ABC):

    def __init__(self, driver: webdriver.Firefox) -> None:
        self.driver = driver

    @abc.abstractmethod
    def get_current_url(self, param: AbcParam) -> str:
        pass

    @abc.abstractmethod
    def fetch_one(self, soup: BeautifulSoup) -> Iterator[dict]:
        pass

    @abc.abstractmethod
    def get_total_count(self, soup: BeautifulSoup) -> str:
        pass

    @abc.abstractmethod
    def get_method(self):
        pass

    def run(self, param: AbcParam):
        method = self.get_method()
        results = []
        while param.alive():
            current_url = self.get_current_url(param=param)
            self.driver.get(url=current_url)
            logging.info(current_url)

            try:
                WebDriverWait(self.driver, 10).until(method)
            except Exception as e:
                logging.error(e)
                continue

            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            results.extend(self.fetch_one(soup=soup))

            if param.can_update_total_count():
                text = self.get_total_count(soup=soup)
                param.set_total_count(self.value(text=text))

            param.set_next()
            time.sleep(random.uniform(5, 9))
            self.save(dest=param.dest, data=results)

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

    def value(self, text: str) -> int:
        count = ''
        for char in text:
            if char.isdigit():
                count += char
        return int(count)
