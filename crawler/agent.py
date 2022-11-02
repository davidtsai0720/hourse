# -*- coding: utf-8 -*-
from enum import Enum

from .base import AbcParam


class QueryParameter(Enum):

    Taipei = {
        'min_price': 800,
        'max_price': 2600,
        'area': 15,
        'city': 'Taipei',
    }

    NewTaipei = {
        'min_price': 800,
        'max_price': 2600,
        'area': 15,
        'city': 'NewTaipei',
    }


class Param(AbcParam):

    def __init__(self, param: dict) -> None:
        self.city: str = param['city']
        self.min_price: int = param['min_price']
        self.max_price: int = param['max_price']
        self.area: str = param['area']
        self.page = 1

    @property
    def size(self) -> int:
        return self._size

    @size.setter
    def size(self, size: int) -> None:
        self._size = size

    def alive(self) -> bool:
        return self.can_update_total_count() or (self.page - 1) * self.size < self.total_count

    def dict(self) -> dict:
        return {
            'city': self.city,
            'min_price': self.min_price,
            'max_price': self.max_price,
            'area': self.area,
            'page': self.page,
        }
