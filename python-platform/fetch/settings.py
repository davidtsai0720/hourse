# -*- coding: utf-8 -*-
from typing import Tuple
from enum import Enum

from .parse import Sinyi, Parent, YungChing
from .parse import parents


class Settings(Enum):

    cities: Tuple[str] = tuple(parents.Settings.city_mapping.value.keys())

    class_mapping: Tuple[Parent] = (YungChing, Sinyi,)

    max_delay_second = 9
    min_delay_second = 5
