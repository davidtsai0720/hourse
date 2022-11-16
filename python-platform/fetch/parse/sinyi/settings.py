# -*- coding: utf-8 -*-
from enum import Enum

from fetch.parse.parents import Node


class Settings(Enum):

    URL = "https://www.sinyi.com.tw"
    page_size = 20
    item = Node(tag="div", class_name="buy-list-item")
    total = Node(tag="div", class_name="d-none d-lg-block")
    address = Node(tag="div", class_name="LongInfoCard_Type_Address")
    hourse_info = Node(tag="div", class_name="LongInfoCard_Type_HouseInfo")
    price = Node(tag="div", class_name="LongInfoCard_Type_Right")
