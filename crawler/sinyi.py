# -*- coding: utf-8 -*-
from enum import Enum
from collections.abc import Iterator
import json

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

from .base import House, AbcParam, Node
from .agent import Param


class Item(Enum):

    URL = 'https://www.sinyi.com.tw/buy/list/{min_price}-{max_price}-price/{area}-up-balconyarea/{city}-city/Taipei-R-mrtline/03-mrt/default-desc/{page}'
    PageSize = 20
    Item = Node('div', 'buy-list-item')
    TotalCount = Node('div', 'd-none d-lg-block')
    Address = Node('div', 'LongInfoCard_Type_Address')
    HourseInfo = Node('div', 'LongInfoCard_Type_HouseInfo')
    Price = Node('div', 'LongInfoCard_Type_Right')


class Sinyi(House):

    def get_current_url(self, param: AbcParam) -> str:
        return Item.URL.value.format(**param.dict())

    def fetchone(self, soup: BeautifulSoup) -> Iterator[dict]:
        for element in soup.find_all(Item.Item.value.tag, class_=Item.Item.value.class_name):
            link = element.find('a')
            link = 'https://www.sinyi.com.tw' + link['href']
            result = {'link': link}

            address = element.find(Item.Address.value.tag, class_=Item.Address.value.class_name)
            result.update(dict(zip(
                ('address', 'age', 'shape'),
                (data.text.strip() for data in address.find_all('span')))))

            hourse_info = element.find(Item.HourseInfo.value.tag, class_=Item.HourseInfo.value.class_name)
            result.update(dict(zip(
                ('area', 'main_area', 'layout', 'floor'),
                (data.text.strip() for data in hourse_info.find_all('span')))))

            price = element.find(Item.Price.value.tag, class_=Item.Price.value.class_name)
            for node in price.find_all('span'):
                if node.text.strip() == '萬':
                    break
                result['price'] = node.text.strip().replace(',', '')

            result['raw'] = json.dumps(result)
            result['price'] = self.value(result['price'])
            result['floor'] = result['floor'].replace('樓', 'F')
            result['section'] = result['address'][3:6]
            result['city'] = result['address'][:3]
            result['address'] = result['address'][6:]
            if result['main_area']:
                result['main_area'] = self.value(result['main_area'])

            if result['area']:
                result['area'] = self.value(result['area'])

            yield result

    def get_total_count(self, soup: BeautifulSoup) -> str:
        node = soup.find(Item.TotalCount.value.tag, class_=Item.TotalCount.value.class_name)
        return node.find('div').text

    def get_method(self):
        return expected_conditions.presence_of_element_located((By.CLASS_NAME, Item.Item.value.class_name))

    def run(self, mymap: dict) -> None:
        param = Param(mymap)
        param.size = Item.PageSize.value
        super().run(param=param)
