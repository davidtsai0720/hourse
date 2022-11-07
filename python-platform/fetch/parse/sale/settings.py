# -*- coding: utf-8 -*-
from enum import Enum

from fetch.parse.parents import Node


class Settings(Enum):

    item = Node('div', 'houseList-item')
    title = Node('div', 'houseList-item-title')
    fields = {
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
    total_count = Node('div', 'houseList-head-title')
    URL = 'https://sale.591.com.tw'
    page_size = 30
    city_mappint = {
        'Taipei': 1,
        'NewTaipei': 3,
    }
