from typing import Union
from collections.abc import Iterator
from decimal import Decimal
import abc
import logging

from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup

from fetch.webdriver import Instance
from .tools import Result
from .settings import Settings


class Parent(abc.ABC):

    def __init__(self, city: str, page: int) -> None:
        self._city = city
        self._page = page

    @property
    def settings(self):
        return Settings

    @property
    def city(self):
        return self._city

    @property
    def page(self):
        return self._page

    @property
    def total_count(self):
        return self._total_count

    @abc.abstractmethod
    def get_method(self):
        pass

    @abc.abstractmethod
    def get_current_url(self) -> str:
        pass

    @abc.abstractmethod
    def get_total_count(self, soup: BeautifulSoup) -> int:
        pass

    @abc.abstractmethod
    def fetchone(self, soup: BeautifulSoup) -> Iterator[dict]:
        pass

    def to_decimal(self, text: str) -> Decimal:
        count = ''
        for char in text:
            if char.isdigit() or char == '.':
                count += char
        return Decimal(count)

    def exec(self, driver: Instance) -> Result:
        method = self.get_method()
        current_url = self.get_current_url()
        instance = driver.get_instance()

        try:
            instance.get(url=current_url)
            logging.info(current_url)
            WebDriverWait(instance, 10).until(method)

        except Exception as e:
            driver.reset()
            assert False, e

        soup = BeautifulSoup(instance.page_source, 'html.parser')
        request = self.fetchone(soup=soup)
        total = self.to_decimal(self.get_total_count(soup))
        return Result(Request=request, Page=self.page, Total=total)
