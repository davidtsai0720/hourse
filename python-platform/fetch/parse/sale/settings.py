# -*- coding: utf-8 -*-
from enum import Enum

from fetch.parse.parents import Node


class Settings(Enum):

    item = Node("div", "houseList-item")
    title = Node("div", "houseList-item-title")
    fields = {
        "main_area": Node(tag="span", class_name="houseList-item-attrs-mainarea"),
        "address": Node(tag="span", class_name="houseList-item-address"),
        "price": Node(tag="div", class_name="houseList-item-price"),
        "section": Node(tag="span", class_name="houseList-item-section"),
        "purpose": Node(tag="span", class_name="houseList-item-attrs-purpose"),
        "layout": Node(tag="span", class_name="houseList-item-attrs-layout"),
        "room": Node(tag="span", class_name="houseList-item-attrs-room"),
        "area": Node(tag="span", class_name="houseList-item-attrs-area"),
        "age": Node(tag="span", class_name="houseList-item-attrs-houseage"),
        "floor": Node(tag="span", class_name="houseList-item-attrs-floor"),
        "shape": Node(tag="span", class_name="houseList-item-attrs-shape"),
    }
    total_count = Node("div", "houseList-head-title")
    URL = "https://sale.591.com.tw"
    page_size = 30
    city_mappint = {
        "Taipei": 1,
        "NewTaipei": 3,
    }
