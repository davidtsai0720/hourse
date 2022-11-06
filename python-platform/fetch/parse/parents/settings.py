# -*- coding: utf-8 -*-
from enum import Enum


class Settings(Enum):

    max_price = 6000
    min_price = 600
    min_area = 6

    city_mapping = {
        'Taipei': '台北市',
        'NewTaipei': '新北市',
    }
