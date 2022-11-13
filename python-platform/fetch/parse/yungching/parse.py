# -*- coding: utf-8 -*-
from collections.abc import Iterator
import json

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

from fetch.parse.parents import Parent
from .settings import Settings


class YungChing(Parent):

    def __init__(self, city: str, page: int) -> None:
        super().__init__(city, page)
        self._city = self.settings.city_mapping.value[city]

    def get_method(self):
        return expected_conditions.presence_of_element_located((
            By.CLASS_NAME,
            Settings.item.value.class_name,
        ))

    def get_current_url(self) -> str:
        return '/'.join((
            f'{Settings.URL.value}/region',
            f'{self.city}-_c',
            f'{self.settings.min_price.value}-{self.settings.max_price.value}_price',
            f'{self.settings.min_area.value}-_pinby',
            f'?pg={self.page}'
        ))

    def get_total_count(self, soup: BeautifulSoup) -> int:
        node = soup.find(
            Settings.total_count.value.tag,
            class_=Settings.total_count.value.class_name,
        )
        return node.text

    def has_next(self) -> bool:
        return self.page * Settings.page_size.value < self.total_count

    def fetchone(self, soup: BeautifulSoup) -> Iterator[dict]:
        for element in soup.find_all(
            Settings.item.value.tag,
            class_=Settings.item.value.class_name,
        ):
            title = element.find(
                Settings.title.value.tag,
                class_=Settings.title.value.class_name,
            )
            result = {
                'title': title.text.strip(),
                'link': title['href'],
            }

            price = element.find(
                Settings.price.value.tag,
                class_=Settings.price.value.class_name,
            )
            result['price'] = price.text.strip()

            address = element.find(
                Settings.address.value.tag,
                class_=Settings.address.value.class_name,
            ).find('span')
            result['address'] = address.text.strip()

            detail = element.find(
                Settings.detail.value.tag,
                class_=Settings.detail.value.class_name,
            )
            if len(detail.find_all('li')) != len(Settings.fields.value):
                continue

            result.update(zip(
                Settings.fields.value,
                (node.text.strip() for node in detail.find_all('li')),
            ))

            if result['floor'] != '':
                result['floor'] = result['floor'].split('~')[1].strip().replace(' ', '')
                result['floor'] = '/'.join(f'{floor}F' for floor in result['floor'][:-1].split('/'))

            result['raw'] = json.dumps(result)
            result['link'] = Settings.URL.value + result['link']
            result['section'] = result['address'][3:6]
            result['city'] = result['address'][:3]

            if result['main_area']:
                result['main_area'] = self.to_decimal(result['main_area'])

            if result['area']:
                result['area'] = self.to_decimal(result['area'])

            result['price'] = self.to_decimal(result['price'].replace(',', ''))
            result['address'] = result['address'][6:]
            result['layout'] = result['room']

            yield result
