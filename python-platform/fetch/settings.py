# -*- coding: utf-8 -*-
from typing import Tuple
from enum import Enum

from .parse import Sinyi, Parent, YungChing


class Settings(Enum):

    cities: Tuple[str] = ('Taipei', 'NewTaipei', )

    class_mapping: Tuple[Parent] = (YungChing, Sinyi,)

    delay = 5
