# -*- coding: utf-8 -*-
from enum import Enum
from collections import defaultdict
from collections.abc import Iterator
import json
import os

import pandas

keys = ('591', 'yungching')


class Section(Enum):

    Taipei = (
        '中正區',
        '萬華區',
        '大同區',
        '中山區',
        '松山區',
        '大安區',
        '信義區',
        '內湖區',
        '南港區',
        '士林區',
        '北投區',
        '文山區',
    )

    NewTaipei = (
        '土城區',
        '雙溪區',
        '鶯歌區',
        '萬里區',
        '三重區',
        '中和區',
        '八里區',
        '蘆洲區',
        '林口區',
        '汐止區',
        '泰山區',
        '淡水區',
        '瑞芳區',
        '石碇區',
        '石門區',
        '五股區',
        '平溪區',
        '貢寮區',
        '坪林區',
        '金山區',
        '三芝區',
        '永和區',
        '新店區',
        '板橋區',
        '樹林區',
        '深坑區',
        '三峽區',
        '烏來區',
        '新莊區',
    )


class Parse:

    @staticmethod
    def walk(src: str) -> Iterator[str, str]:
        wd = os.path.join(os.getcwd(), 'output')
        result = defaultdict(list)
        for root, _, files in os.walk(wd):
            for file in files:
                yield root, file

    @classmethod
    def normalize591(cls, source: list) -> Iterator[dict]:
        dup_keys = ('address', 'shape', 'floor', 'age', 'section')
        keys = ('link', 'layout', 'address', 'section', 'price', 'floor', 'shape', 'age', 'area', 'main_area')
        visit = set()
        for data in source:
            key = ':'.join(data[key] for key in dup_keys)
            if key in visit:
                continue
            result = {key: data[key] for key in keys}
            result['link']: str = 'https://sale.591.com.tw' + result['link']
            result['section']: str = result['section'].replace('-', '')
            yield result
            visit.add(key)

    @staticmethod
    def normalizeYC(source: list) -> Iterator[dict]:
        keys = ('link', 'layout', 'address', 'section', 'price', 'floor', 'shape', 'age', 'area', 'main_area')
        for data in source:
            result = {key: data[key] for key in keys if key in data}
            result['link'] = 'https://buy.yungching.com.tw' + result['link']
            result['section'] = result['address'][3:6]
            result['address'] = result['address'][6:]
            yield result

    @classmethod
    def fetch_all(cls, src: str) -> Iterator[dict]:
        for root, file in cls.walk(src):
            name = os.path.join(root, file)
            with open(name, 'r') as f:
                data = json.loads(f.read())

                if file.startswith('591'):
                    yield from cls.normalize591(data)

                elif file.startswith('yungching'):
                    yield from cls.normalizeYC(data)

    @staticmethod
    def value(text: str) -> float:
        number = ''
        for char in text:
            if char.isdigit():
                number += char
            elif char == '.':
                number += char
        return float(number)

    @staticmethod
    def section(text: str) -> str:
        if text in Section.NewTaipei.value:
            return '新北市' + text

        if text in Section.Taipei.value:
            return '台北市' + text

        return text

    @classmethod
    def filter(cls, source: Iterator[dict]) -> Iterator[dict]:
        results = []
        for row in source:

            floor = row['floor'].split('/')
            if len(floor) != 2:
                continue

            if floor[0] == floor[1]:
                continue

            if not floor[0][0].isdigit():
                continue

            if int(floor[0][0]) < 3:
                continue

            if row['main_area'] == '':
                continue

            if row['age'] in ('', '不詳') or row['age'].endswith('月'):
                continue

            row['main_area'] = cls.value(row['main_area'])
            row['area'] = cls.value(row['area'])
            row['section'] = cls.section(row['section'])
            row['address'] = row['section'] + row['address']
            row['price'] = int(row['price'].split('  ')[-1].replace(',', '').split(' ')[0])

            results.append(row)
        return results
