# -*- coding: utf-8 -*-
from collections import namedtuple
from collections.abc import Iterator
import abc
import random
import logging
import time
import decimal

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup

from postgres.postgres import Postgres

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


class House(abc.ABC):

    def __init__(self, driver: webdriver.Firefox, conn) -> None:
        self.driver = driver
        self.conn = conn
        self.section: dict = {}

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
            for result in self.fetch_one(soup=soup):
                self.insert(result)

            if param.can_update_total_count():
                text = self.get_total_count(soup=soup)
                param.set_total_count(self.value(text=text))

            param.set_next()
            time.sleep(random.uniform(5, 9))

    def section_id(self, section: str) -> int:
        try:
            return self.section[section]
        except Exception:
            with self.conn.cursor() as cursor:
                cursor.execute('SELECT id FROM section WHERE name = %s', (section,))
                record = cursor.fetchone()
                self.section[section] = record[0]
            return self.section[section]

    def insert(self, mymap: dict) -> None:
        keys = ('section_id', 'link', 'layout', 'address', 'price', 'floor', 'shape', 'age', 'area', 'main_area', 'raw')
        data = []
        for key in keys:
            value = mymap[key] if key != 'section_id' else self.section_id(mymap['section'])
            if not mymap['main_area']:
                mymap['main_area'] = None
            data.append(value)
        Postgres.insert(self.conn, data)

    def value(self, text: str) -> decimal.Decimal:
        count = ''
        for char in text:
            if char.isdigit() or char == '.':
                count += char
        return decimal.Decimal(count)
