# -*- coding: utf-8 -*-
from collections.abc import Iterator
import json

from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions

from fetch.parse.parents import Parent
from .settings import Settings


class Sinyi(Parent):

    def get_method(self):
        return expected_conditions.presence_of_element_located((
            By.CLASS_NAME,
            Settings.item.value.class_name,
        ))

    def get_current_url(self) -> str:
        return '/'.join((
            f'{Settings.URL.value}/buy/list',
            f'{self.settings.min_price.value}-{self.settings.max_price.value}-price',
            f'{self.settings.min_area.value}-up-balconyarea',
            f'{self.city}-city',
            f'Taipei-R-mrtline/03-mrt/default-desc/{self.page}',
        ))

    def get_total_count(self, soup: BeautifulSoup) -> int:
        node = soup.find(
            Settings.total.value.tag,
            class_=Settings.total.value.class_name,
        )
        return node.find('div').text

    def has_next(self) -> bool:
        return (self.page - 1) * Settings.page_size.value < self.total_count

    def fetchone(self, soup: BeautifulSoup) -> Iterator[dict]:
        for element in soup.find_all(
            Settings.item.value.tag,
            class_=Settings.item.value.class_name,
        ):
            link = element.find('a')
            link = Settings.URL.value + link['href']
            result = {'link': link}

            address = element.find(
                Settings.address.value.tag,
                class_=Settings.address.value.class_name,
            )
            result.update(zip(
                ('address', 'age', 'shape'),
                (data.text.strip() for data in address.find_all('span'))))

            hourse_info = element.find(
                Settings.hourse_info.value.tag,
                class_=Settings.hourse_info.value.class_name,
            )
            result.update(zip(
                ('area', 'main_area', 'layout', 'floor'),
                (data.text.strip() for data in hourse_info.find_all('span'))))

            price = element.find(
                Settings.price.value.tag,
                class_=Settings.price.value.class_name,
            )

            for node in price.find_all('span'):
                if node.text.strip() == '萬':
                    break
                result['price'] = node.text.strip().replace(',', '')

            result['raw'] = json.dumps(result)
            result['price'] = self.to_decimal(result['price'])
            result['floor'] = result['floor'].replace('樓', 'F')
            result['section'] = result['address'][3:6]
            result['city'] = result['address'][:3]
            result['address'] = result['address'][6:]

            if result['main_area']:
                result['main_area'] = self.to_decimal(result['main_area'])

            if result['area']:
                result['area'] = self.to_decimal(result['area'])

            yield result
