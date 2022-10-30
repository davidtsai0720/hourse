# -*- coding: utf-8 -*-
from collections.abc import Iterator
from enum import Enum

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

from .base import House, Node, AbcParam


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

    def get_method(self):
        return expected_conditions.presence_of_element_located((By.CLASS_NAME, Item.Item.value.class_name))

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

            if updates['floor'] != '':
                updates['floor'] = updates['floor'].split('~')[1].strip().replace(' ', '')
                updates['floor'] = '/'.join(f'{floor}F' for floor in updates['floor'][:-1].split('/'))

            result.update(updates)
            yield result

    def get_current_url(self, param: AbcParam) -> str:
        return Item.URL.value.format(**param.dict())

    def get_total_count(self, soup: BeautifulSoup) -> str:
        node = soup.find(Item.TotalCount.value.tag, class_=Item.TotalCount.value.class_name)
        return node.text

    def run(self, mymap: dict) -> None:
        param = Param(mymap)
        super().run(param=param)


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
