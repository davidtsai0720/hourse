# -*- coding: utf-8 -*-
from decimal import Decimal


class CreateHourse:
    __slots__ = (
        "_city",
        "_section",
        "_link",
        "_layout",
        "_address",
        "_price",
        "_floor",
        "_shape",
        "_age",
        "_area",
        "_main_area",
        "_raw")

    @property
    def city(self):
        return self._city

    @city.setter
    def city(self, city: str):
        self._city = city

    @property
    def section(self):
        return self._section

    @section.setter
    def section(self, section: str):
        self._section = section

    @property
    def link(self):
        return self._link

    @link.setter
    def link(self, link: str):
        self._link = link

    @property
    def raw(self):
        return self._raw

    @raw.setter
    def raw(self, raw: str):
        self._raw = raw

    @property
    def main_area(self):
        return self._main_area

    @main_area.setter
    def main_area(self, main_area: str):
        self._main_area = main_area

    @property
    def area(self):
        return self._area

    @area.setter
    def area(self, area: str):
        self._area = area

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, age: str):
        self._age = age

    @property
    def shape(self):
        return self._shape

    @shape.setter
    def shape(self, shape: str):
        self._shape = shape

    @property
    def floor(self):
        return self._floor

    @floor.setter
    def floor(self, floor: str):
        self._floor = floor

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, price: Decimal):
        self._price = price

    @property
    def address(self):
        return self._address

    @address.setter
    def address(self, address: str):
        self._address = address

    @property
    def layout(self):
        return self._layout

    @layout.setter
    def layout(self, layout: str):
        self._layout = layout
