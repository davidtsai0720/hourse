# -*- coding: utf-8 -*-
from enum import Enum


class Settings(Enum):

    max_price = 3000
    min_price = 800
    min_area = 12
    city_mapping = {
        "Taipei": "台北市",
        "NewTaipei": "新北市",
    }
