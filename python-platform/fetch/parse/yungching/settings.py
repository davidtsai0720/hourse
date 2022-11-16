# -*- coding: utf-8 -*-
from enum import Enum

from fetch.parse.parents import Node


class Settings(Enum):

    URL = "https://buy.yungching.com.tw"
    page_size = 30
    item = Node(tag="li", class_name="m-list-item")
    title = Node(tag="a", class_name="item-title")
    detail = Node(tag="ul", class_name="item-info-detail")
    fields = ("shape", "age", "floor", "field1", "main_area", "area", "room", "field2", "field3")
    address = Node(tag="div", class_name="item-description")
    price = Node(tag="div", class_name="price")
    total_count = Node(tag="a", class_name="list-filter is-first active ng-isolate-scope")
