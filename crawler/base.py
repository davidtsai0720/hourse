# -*- coding: utf-8 -*-
from collections import namedtuple
from collections.abc import Iterator
from enum import Enum
import json
import abc
import random
import logging
import time
import decimal

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


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

    def can_update_total_count(self) -> bool:
        return self.__dict__.get('total_count', None) is None

    def set_next(self) -> None:
        self.page += 1

    def set_total_count(self, num: int) -> None:
        self.total_count = num


class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        return super(DecimalEncoder, self).default(o)


class Setting(Enum):

    driverPath = '/usr/bin/geckodriver'


class House(abc.ABC):

    @abc.abstractmethod
    def get_current_url(self, param: AbcParam) -> str:
        pass

    @abc.abstractmethod
    def fetchone(self, soup: BeautifulSoup) -> Iterator[dict]:
        pass

    @abc.abstractmethod
    def get_total_count(self, soup: BeautifulSoup) -> str:
        pass

    @abc.abstractmethod
    def get_method(self):
        pass

    def run(self, param: AbcParam):
        method = self.get_method()

        while param.alive():
            current_url = self.get_current_url(param=param)
            try:
                self.driver.get(url=current_url)
                logging.info(current_url)
                WebDriverWait(self.driver, 10).until(method)
            except Exception as e:
                logging.error(e)
                self.driver.close()
                self.driver.quit()
                del self._driver

            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            for result in self.fetchone(soup=soup):
                try:
                    self.insert(result)
                except Exception as e:
                    logging.error(f'error: {e}, data is {result}')

            if param.can_update_total_count():
                text = self.get_total_count(soup=soup)
                param.set_total_count(self.value(text=text))

            param.set_next()
            time.sleep(random.uniform(5, 9))

        self.driver.close()
        self.driver.quit()

    def insert(self, data: dict) -> None:
        headers = {'content-type': 'application/json; charset=utf-8'}
        retry = Retry(connect=3, backoff_factor=0.5)
        adapter = HTTPAdapter(max_retries=retry)
        session = requests.Session()
        session.mount('http://', adapter)
        try:
            resp = session.post(
                'http://localhost:8080/hourse',
                headers=headers,
                data=json.dumps(data, cls=DecimalEncoder))
            assert resp.status_code == 204, resp.json()
        except Exception as e:
            print(e)
            time.sleep(5)
        finally:
            resp.close()
            session.close()

    def value(self, text: str) -> decimal.Decimal:
        count = ''
        for char in text:
            if char.isdigit() or char == '.':
                count += char
        return decimal.Decimal(count)

    @property
    def driver(self):
        try:
            return self._driver
        except AttributeError:
            options = FirefoxOptions()
            options.headless = True
            service = Service(Setting.driverPath.value)
            driver = webdriver.Firefox(service=service, options=options)
            self._driver = driver
            return self._driver
