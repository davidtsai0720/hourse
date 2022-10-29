# -*- coding: utf-8 -*-
from collections import namedtuple
from enum import Enum
import logging
import json
import time

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from .base import House, URL

Node = namedtuple('Node', ('tag', 'class_name'))
QueryParam = namedtuple('QueryParam', ('params', 'dest'))


class Element(Enum):

    Item = Node('div', 'houseList-item')
    Title = Node('div', 'houseList-item-title')
    Elements = {
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


class Sale591(House):

    @property
    def base_url(self) -> str:
        return 'https://sale.591.com.tw'

    def fetch_one(self, soup: BeautifulSoup):
        for input in soup.find_all(
                Element.Item.value.tag,
                class_=Element.Item.value.class_name):

            result = {}
            titleNode = input.find(
                Element.Title.value.tag,
                class_=Element.Title.value.class_name)

            result['title'] = titleNode.text.strip()
            result['link'] = titleNode.a['href']
            for key, node in Element.Elements.value.items():
                item = input.find(node.tag, class_=node.class_name)
                result[key] = '' if item is None else item.text.strip()

            yield result

    def run(self, args: QueryParam) -> None:
        method = expected_conditions.presence_of_element_located(
            (By.CLASS_NAME, Element.Item.value.class_name))

        params = args.params
        results = []
        params['firstRow'] = 0

        while 'totalRows' not in params or params['firstRow'] < params['totalRows']:
            url = URL.build(self.base_url, params=params)
            self.driver.get(url)
            print(self.driver.current_url)
            try:
                WebDriverWait(self.driver, 10).until(method)
            except Exception as e:
                logging.warning(e)
                return
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            results.extend(self.fetch_one(soup=soup))

            if 'totalRows' not in params:
                content = soup.find(
                    Element.TotalRows.value.tag,
                    class_=Element.TotalRows.value.class_name)
                count = ''
                for char in content.text:
                    if char.isdigit():
                        count += char
                params['totalRows'] = int(count)

            params['firstRow'] += 30
            time.sleep(5)

            with open(args.dest, 'w') as f:
                f.write(json.dumps(results))


class Query(Enum):

    Taipei = [
        QueryParam({
            'shType': 'list',
            'regionid': 1,
            'kind': 9,
            'price': '1000$_2600$',
            'area': '18$_$',
            'houseage': '25$_45$',
            'shape': 0,
        }, 'taipei_591.json'),
    ]

    NewTaipei = [
        QueryParam({
            'shType': 'list',
            'regionid': 3,
            'kind': 9,
            'price': '1000$_2000$',
            'area': '25$_$',
            'houseage': '$_30$',
            'shape': 0,
            'section': '38,37,26,34,44',
        }, 'new_tapite_591_1.json'),
        QueryParam({
            'shType': 'list',
            'regionid': 3,
            'kind': 9,
            'price': '1000$_2000$',
            'area': '25$_$',
            'houseage': '$_30$',
            'shape': 0,
            'section': '46,27,43',
        }, 'new_tapite_591_2.json'),
    ]
