# -*- coding: utf-8 -*-
from audioop import add
from collections.abc import Iterator
from curses.ascii import isdigit
from enum import Enum
import random
import logging
import time

from bs4 import BeautifulSoup

from .base import House, Node
# https://buy.yungching.com.tw/region/台北市-_c/1000-2600_price/18-_pinby/


class Param:

    def __init__(self, param: dict) -> None:
        self.city: str = param['city']
        self.min_price: int = param['min_price']
        self.max_price: int = param['max_price']
        self.area: str = param['area']
        self.page = 1
        self.dest: str = param['dest']

    def set_total_count(self, num: int) -> None:
        self.total_count = num

    @property
    def alive(self) -> bool:
        return self.can_update_total or self.page * Item.PageSize.value < self.total_count

    @property
    def can_update_total(self) -> bool:
        return self.__dict__.get('total_count', None) is None

    @property
    def dict(self) -> dict:
        return {
            'city': self.city,
            'min_price': self.min_price,
            'max_price': self.max_price,
            'area': self.area,
            'page': self.page,
        }


class Item(Enum):

    URL = 'https://buy.yungching.com.tw/region/{city}-_c/{min_price}-{max_price}_price/{area}-_pinby/?pg={page}'
    TotalCount = Node('a', 'list-filter is-first active ng-isolate-scope')
    PageSize = 30
    Item = Node('li', 'm-list-item')
    Title = Node('a', 'item-title')
    Detail = Node('ul', 'item-info-detail')
    Fields = ('shape', 'age', 'floor', 'field1', 'main_area', 'area', 'room', 'field2', 'field3')
    Address = Node('div', 'item-description')
    Price = Node('div', 'price')


class YungChing(House):

    def fetch_one(self, soup: BeautifulSoup) -> Iterator[dict]:
        for element in soup.find_all(Item.Item.value.tag, class_=Item.Item.value.class_name):
            title = element.find(Item.Title.value.tag, class_=Item.Title.value.class_name)
            result = {
                'title': title.text.strip(),
                'link': title["href"],
            }

            price = element.find(Item.Price.value.tag, class_=Item.Price.value.class_name)
            result['price'] = price.text.strip()

            address = element.find(Item.Address.value.tag, class_=Item.Address.value.class_name).find('span')
            result['address'] = address.text.strip()

            detail = element.find(Item.Detail.value.tag, class_=Item.Detail.value.class_name)
            updates = dict(zip(Item.Fields.value, (node.text.strip() for node in detail.find_all('li'))))
            updates['floor'] = updates['floor'].split('~')[1].strip().replace(' ', '')
            updates['floor'] = '/'.join(f'{floor}F' for floor in updates['floor'][:-1].split('/'))

            result.update(updates)
            yield result

    def run(self, mymap: dict) -> None:
        param = Param(mymap)
        results = []
        while param.alive:
            url = Item.URL.value.format(**param.dict)
            self.driver.get(url=url)
            logging.info(self.driver.current_url)

            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            results.extend(self.fetch_one(soup=soup))

            if param.can_update_total:
                node = soup.find(Item.TotalCount.value.tag, class_=Item.TotalCount.value.class_name)
                param.set_total_count(self.value(node.text))

            param.page += 1
            time.sleep(random.uniform(5, 9))
            self.save(dest=param.dest, data=results)


class Query(Enum):

    Taipei = {
        'city': '台北市',
        'min_price': 1000,
        'max_price': 2600,
        'area': 18,
        'dest': 'yungchingTaipei.json',
    }

    NewTaipei = {
        'city': '新北市',
        'min_price': 800,
        'max_price': 2000,
        'area': 25,
        'dest': 'yungchingNewTaipei.json',
    }
