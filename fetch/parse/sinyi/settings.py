from enum import Enum

from fetch.parse.tools import Node


class Settings(Enum):

    URL = 'https://www.sinyi.com.tw'
    page_size = 20
    item = Node('div', 'buy-list-item')
    total = Node('div', 'd-none d-lg-block')
    address = Node('div', 'LongInfoCard_Type_Address')
    hourse_info = Node('div', 'LongInfoCard_Type_HouseInfo')
    price = Node('div', 'LongInfoCard_Type_Right')
