# -*- coding: utf-8 -*-
from collections.abc import Iterator
from enum import Enum
import json

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

from .base import House, Node, AbcParam
from .agent import Param


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

    def fetchone(self, soup: BeautifulSoup) -> Iterator[dict]:
        for element in soup.find_all(Item.Item.value.tag, class_=Item.Item.value.class_name):
            title = element.find(Item.Title.value.tag, class_=Item.Title.value.class_name)
            result = {
                'title': title.text.strip(),
                'link': title['href'],
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

            result['raw'] = json.dumps(result)
            result['link'] = 'https://buy.yungching.com.tw' + result['link']
            result['section'] = result['address'][3:6]
            result['city'] = result['address'][:3]
            if result['main_area']:
                result['main_area'] = self.value(result['main_area'])

            if result['area']:
                result['area'] = self.value(result['area'])

            result['price'] = self.value(result['price'].replace(',', ''))
            result['address'] = result['address'][6:]
            result['layout'] = result['room']

            yield result

    def get_current_url(self, param: AbcParam) -> str:
        return Item.URL.value.format(**param.dict())

    def get_total_count(self, soup: BeautifulSoup) -> str:
        node = soup.find(Item.TotalCount.value.tag, class_=Item.TotalCount.value.class_name)
        return node.text

    def run(self, mymap: dict) -> None:
        param = Param(mymap)
        param.size = Item.PageSize.value
        super().run(param=param)
