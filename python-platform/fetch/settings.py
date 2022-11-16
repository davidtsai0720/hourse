# -*- coding: utf-8 -*-
from typing import Tuple, List
from enum import Enum

# from .parse import Sinyi, Parent, YungChing, Sale
from .parse import Parent
from .parse import parents


class Settings(Enum):

    cities: Tuple[str] = tuple(parents.Settings.city_mapping.value.keys())
    class_mapping: List[Parent] = Parent.class_group
    max_delay_second = 9
    min_delay_second = 5
