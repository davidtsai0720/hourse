# -*- coding: utf-8 -*-
from collections.abc import Iterator
import json

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

from fetch.parse.parents import Parent
from .settings import Settings
from .tools import URL


class Sale(Parent):

    def get_method(self):
        return expected_conditions.presence_of_element_located((
            By.CLASS_NAME,
            Settings.item.value.class_name))

    def get_current_url(self) -> str:
        return URL.build(host=Settings.URL.value, params={
            'shType': 'list',
            'regionid': Settings.city_mappint.value.get(self.city, ''),
            'kind': 9,
            'price': f'{self.settings.min_price.value}$_{self.settings.max_price.value}$',
            'area': f'{self.settings.min_area.value}$_$',
            'firstRow': self.page * Settings.page_size.value,
            'totalRows': 0,
        })

    def get_total_count(self, soup: BeautifulSoup) -> int:
        node = soup.find(
            Settings.total_count.value.tag,
            class_=Settings.total_count.value.class_name,
        )
        return node.text

    def has_next(self) -> bool:
        return (self.page - 1) * Settings.page_size.value < self.total_count

    def fetchone(self, soup: BeautifulSoup) -> Iterator[dict]:
        for input in soup.find_all(
            Settings.item.value.tag,
            class_=Settings.item.value.class_name,
        ):
            titleNode = input.find(
                Settings.title.value.tag,
                class_=Settings.title.value.class_name,
            )

            result = {
                'title': titleNode.text.strip(),
                'link': titleNode.a['href'],
            }

            if 'newhouse' in result['link']:
                continue

            for key, node in Settings.fields.value.items():
                item = input.find(node.tag, class_=node.class_name)
                result[key] = '' if item is None else item.text.strip()

            result['section'] = result['section'].replace('-', '')
            result['raw'] = json.dumps(result)
            result['link'] = Settings.URL.value + result['link']
            result['city'] = self.city

            if result['main_area']:
                result['main_area'] = self.to_decimal(result['main_area'])

            if result['area']:
                result['area'] = self.to_decimal(result['area'])

            if result['price']:
                result['price'] = self.to_decimal(result['price'].split('  ')[-1])

            yield result
