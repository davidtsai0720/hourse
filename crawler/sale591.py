# -*- coding: utf-8 -*-
from enum import Enum
from collections.abc import Iterator
import json

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

from .base import House, URL, Node, AbcParam


class Param(AbcParam):

    def __init__(self, param: dict) -> None:
        self.shType: str = 'list'
        self.regionid: int = param['regionid']
        self.kind: int = param['kind']
        self.price: str = param['price']
        self.area: str = param['area']
        self.age: str = param['houseage']
        self.dest: str = param['dest']
        self.page = 1
        if 'section' in param:
            self.section: str = param['section']

    def alive(self) -> bool:
        return self.can_update_total_count() or self.page * Item.PageSize.value < self.total_count

    def dict(self) -> dict:
        result = {
            'shType': self.shType,
            'regionid': self.regionid,
            'kind': self.kind,
            'price': self.price,
            'area': self.area,
            'houseage': self.age,
            'firstRow': self.page * Item.PageSize.value,
        }

        if self.__dict__.get('section', None) is not None:
            result['section']: str = self.section

        if self.__dict__.get('total_count', None) is not None:
            result['totalRows']: int = self.total_count

        return result


class Item(Enum):

    Item = Node('div', 'houseList-item')
    Title = Node('div', 'houseList-item-title')
    Fields = {
        'purpose': Node('span', 'houseList-item-attrs-purpose'),
        'room': Node('span', 'houseList-item-attrs-room'),
        'area': Node('span', 'houseList-item-attrs-area'),
        'main_area': Node('span', 'houseList-item-attrs-mainarea'),
        'address': Node('span', 'houseList-item-address'),
        'layout': Node('span', 'houseList-item-attrs-layout'),
        'section': Node('span', 'houseList-item-section'),
        'age': Node('span', 'houseList-item-attrs-houseage'),
        'price': Node('div', 'houseList-item-price'),
        'floor': Node('span', 'houseList-item-attrs-floor'),
        'shape': Node('span', 'houseList-item-attrs-shape'),
    }
    TotalRows = Node('div', 'houseList-head-title')
    URL = 'https://sale.591.com.tw'
    PageSize = 30


class Sale591(House):

    def get_method(self):
        return expected_conditions.presence_of_element_located((By.CLASS_NAME, Item.Item.value.class_name))

    def fetchone(self, soup: BeautifulSoup) -> Iterator[dict]:
        for input in soup.find_all(Item.Item.value.tag, class_=Item.Item.value.class_name):
            result = {}
            titleNode = input.find(Item.Title.value.tag, class_=Item.Title.value.class_name)

            result['title'] = titleNode.text.strip()
            result['link'] = titleNode.a['href']

            if 'newhouse' in result['link']:
                continue

            for key, node in Item.Fields.value.items():
                item = input.find(node.tag, class_=node.class_name)
                result[key] = '' if item is None else item.text.strip()

            result['raw'] = json.dumps(result)
            result['section'] = result['section'][:-1]
            result['link'] = 'https://sale.591.com.tw' + result['link']

            if result['main_area']:
                result['main_area'] = self.value(result['main_area'])

            if result['area']:
                result['area'] = self.value(result['area'])

            if result['price']:
                result['price'] = int(self.value(result['price'].split('  ')[-1]))
            yield result

    def get_current_url(self, param: AbcParam) -> str:
        return URL.build(Item.URL.value, params=param.dict())

    def get_total_count(self, soup: BeautifulSoup) -> str:
        node = soup.find(Item.TotalRows.value.tag, class_=Item.TotalRows.value.class_name)
        return node.text

    def run(self, mymap: dict) -> None:
        param = Param(mymap)
        super().run(param=param)


class Query(Enum):

    Taipei = {
        'regionid': 1,
        'kind': 9,
        'price': '1000$_2600$',
        'area': '18$_$',
        'houseage': '25$_45$',
        'dest': '591Taipei.json'
    }

    NewTaipei = {
        'regionid': 3,
        'kind': 9,
        'price': '800$_2000$',
        'area': '25$_$',
        'houseage': '$_30$',
        'dest': '591NewTaipei.json',
    }
