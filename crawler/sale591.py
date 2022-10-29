# -*- coding: utf-8 -*-
from enum import Enum
from collections.abc import Iterator
import random
import logging
import time

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from .base import House, URL, Node


class Param:

    def __init__(self, param: dict) -> None:
        self.shType: str = 'list'
        self.regionid: int = param['regionid']
        self.kind: int = param['kind']
        self.price: str = param['price']
        self.area: str = param['area']
        self.houseage: str = param['houseage']
        self.dest: str = param['dest']
        self.firstRow = 0
        if 'section' in param:
            self.section: str = param['section']

    def set_firstRow(self, num: int) -> None:
        self.firstRow = num

    def set_totalRows(self, num: int) -> None:
        self.totalRows = num

    @property
    def alive(self) -> bool:
        return self.can_update_total or self.firstRow < self.totalRows

    @property
    def can_update_total(self) -> bool:
        return self.__dict__.get('totalRows', None) is None

    @property
    def dict(self) -> dict:
        result = {
            'shType': self.shType,
            'regionid': self.regionid,
            'kind': self.kind,
            'price': self.price,
            'area': self.area,
            'houseage': self.houseage,
            'firstRow': self.firstRow,
        }

        if self.__dict__.get('section', None) is not None:
            result['section']: str = self.section

        if self.__dict__.get('totalRows', None) is not None:
            result['totalRows']: int = self.totalRows

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


method = expected_conditions.presence_of_element_located((By.CLASS_NAME, Item.Item.value.class_name))


class Sale591(House):

    def fetch_one(self, soup: BeautifulSoup) -> Iterator[dict]:
        for input in soup.find_all(Item.Item.value.tag, class_=Item.Item.value.class_name):
            result = {}
            titleNode = input.find(Item.Title.value.tag, class_=Item.Title.value.class_name)

            result['title'] = titleNode.text.strip()
            result['link'] = titleNode.a['href']
            for key, node in Item.Fields.value.items():
                item = input.find(node.tag, class_=node.class_name)
                result[key] = '' if item is None else item.text.strip()

            yield result

    def run(self, mymap: dict) -> None:
        param = Param(mymap)
        results = []
        while param.alive:
            current_url = URL.build(Item.URL.value, params=param.dict)
            logging.info(current_url)
            self.driver.get(current_url)

            try:
                WebDriverWait(self.driver, 10).until(method)
            except Exception as e:
                logging.error(e)
                continue

            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            results.extend(self.fetch_one(soup=soup))

            if param.can_update_total:
                node = soup.find(Item.TotalRows.value.tag, class_=Item.TotalRows.value.class_name)
                param.set_totalRows(self.value(node.text))

            param.set_firstRow(param.firstRow + Item.PageSize.value)
            time.sleep(random.uniform(5, 9))
            self.save(dest=param.dest, data=results)


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
