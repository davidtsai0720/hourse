# -*- coding: utf-8 -*-
from enum import Enum
from collections.abc import Iterator

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

from .base import House, URL, Node, AbcParam


class Param(AbcParam):

    def __init__(self, param: dict) -> None:
        self.city: str = param['city']
        self.min_price: int = param['min_price']
        self.max_price: int = param['max_price']
        self.area: str = param['area']
        self.dest: str = param['dest']
        self.page = 1

    def alive(self) -> bool:
        return self.can_update_total_count() or (self.page - 1) * Item.PageSize.value < self.total_count

    def dict(self) -> dict:
        return {
            'city': self.city,
            'min_price': self.min_price,
            'max_price': self.max_price,
            'area': self.area,
            'page': self.page,
        }


class Item(Enum):

    URL = 'https://www.sinyi.com.tw/buy/list/{min_price}-{max_price}-price/{area}-up-balconyarea/{city}-city/Taipei-R-mrtline/03-mrt/default-desc/1'
    PageSize = 20


class Sinyi(House):

    def get_current_url(self, param: AbcParam) -> str:
        return Item.URL.value.format(**param.dict())

    def fetch_one(self, soup: BeautifulSoup) -> Iterator[dict]:
        return super().fetch_one(soup)

    def get_total_count(self, soup: BeautifulSoup) -> str:
        return super().get_total_count(soup)

    def get_method(self):
        return super().get_method()

    def run(self, mymap: dict):
        param = Param(mymap)
        return super().run(param=param)


class Query(Enum):

    Taipei = {
        'min_price': 1000,
        'max_price': 2600,
        'area': 18,
        'city': 'Taipei',
        'dest': 'sinyiTaipei.json',
    }

    NewTaipei = {
        'min_price': 1000,
        'max_price': 2600,
        'area': 18,
        'city': 'NewTaipei',
        'dest': 'sinyiTaipei.json',
    }
