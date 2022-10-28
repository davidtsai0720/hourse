# -*- coding: utf-8 -*-
import logging
import json
import time

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from .base import Base

URL = "https://sale.591.com.tw/?shType=list&regionid=1&kind=9&price=1000$_2600$&area=18$_$&houseage=25$_45$&shape=0"


class Element:

    def __init__(self, element) -> None:
        self.element = element

    def fetch(self, clssType: str, className: str):
        item = self.element.find(clssType, class_=className)
        return "" if item is None else item.text.strip()

    @property
    def title(self):
        title = self.element.find('div', class_='houseList-item-title')
        return title.text.strip()

    @property
    def link(self):
        title = self.element.find('div', class_='houseList-item-title')
        return title.a['href']

    @property
    def purpose(self):
        return self.fetch('span', 'houseList-item-attrs-purpose')

    @property
    def room(self):
        return self.fetch('span', 'houseList-item-attrs-room')

    @property
    def area(self):
        return self.fetch('span', 'houseList-item-attrs-area')

    @property
    def mainarea(self):
        return self.fetch('span', 'houseList-item-attrs-mainarea')

    @property
    def address(self):
        return self.fetch('span', 'houseList-item-address')

    @property
    def layout(self):
        return self.fetch('span', 'houseList-item-attrs-layout')

    @property
    def section(self):
        return self.fetch('span', 'houseList-item-section').replace('-', '')

    @property
    def age(self):
        return self.fetch('span', 'houseList-item-attrs-houseage')

    @property
    def price(self):
        return self.fetch('div', 'houseList-item-price')

    @property
    def floor(self):
        return self.fetch('span', 'houseList-item-attrs-floor')

    @property
    def shape(self):
        return self.fetch('span', 'houseList-item-attrs-shape')

    @property
    def dict(self):
        return {
            'Name': self.title,
            'Link': self.link,
            'Type': self.shape,
            'Room': self.room,
            'Floor': self.floor,
            'Area': self.area,
            'MainArea': self.mainarea,
            'Layout': self.layout,
            'Price': self.price,
            'Location': self.section,
            'Address': self.address,
            'Age': self.age,
        }


class Rent(Base):

    file = 'rent.json'

    def fetch_one(self, soup):
        for element in soup.find_all('div', class_='houseList-item'):
            data = Element(element)
            yield data.dict

    def run(self) -> None:
        self.driver.get(URL)
        method = expected_conditions.presence_of_element_located(
            (By.CLASS_NAME, 'houseList-item'))
        candidate = []
        visits = []
        while len(visits) == 0 or visits[-1] != self.driver.current_url:
            print(self.driver.current_url)
            visits.append(self.driver.current_url)
            try:
                WebDriverWait(self.driver, 10).until(method)
            except Exception as e:
                logging.warning(e)
                return
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            candidate.extend(self.fetch_one(soup=soup))
            element = self.driver.find_element(By.CLASS_NAME, 'pageNext')
            self.driver.execute_script('arguments[0].click();', element)
            with open(self.file, 'w') as f:
                f.write(json.dumps(candidate))
            time.sleep(5)
