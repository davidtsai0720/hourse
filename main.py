#! ./venv/bin/python3.11
# -*- coding: utf-8 -*-
import json

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver import FirefoxOptions
import pandas

from house import rent

driverPath = '/usr/bin/geckodriver'


def fetchRent() -> None:
    opts = FirefoxOptions()
    opts.headless = True
    service = Service(driverPath)
    driver = webdriver.Firefox(service=service, options=opts)
    obj = rent.Sale591(driver=driver)

    for data in rent.Query:
        for param in data.value:
            obj.run(param)

    driver.close()
    driver.quit()


class DataArrange:

    @staticmethod
    def isValid(data: dict) -> bool:
        if data['Floor'] != '':
            current, maximum = data['Floor'].split('/')
            if current == maximum:
                return False

            if current[0] in ('1', '2'):
                return False

            if not current[0].isdigit():
                return False

            if data['Type'] == '公寓' and current[0] > '3':
                return False

        if data['MainArea'] == '':
            return False

        if float(data['MainArea'][2:-1]) < 23:
            return False

        if int(data['Age'][:-1]) > 40:
            return False

        return True

    @classmethod
    def source(cls, src: str, prefix: str) -> pandas.DataFrame:
        with open(src, 'r') as f:
            out = json.loads(f.read())

        memory = set()
        array = []
        for data in out:
            key = (data['Address'], data['Price'])
            if key in memory:
                continue

            if not cls.isValid(data):
                continue

            data['Link'] = prefix + data['Link']

            memory.add(key)
            array.append(data)
        return pandas.DataFrame(array)

    @staticmethod
    def saveXLSX(src: pandas.DataFrame, dest: str) -> None:
        output = pandas.DataFrame()
        for candidate in src.groupby(['Location', 'Age', 'Type']):
            df = candidate[1].sort_values(by=['MainArea'])
            output = pandas.concat([output, df])
        output.to_excel(dest)

    @classmethod
    def exec(cls, src: str, dest: str, prefix: str) -> None:
        source = cls.source(src=src, prefix=prefix)
        cls.saveXLSX(src=source, dest=dest)


# 2000+11500+2655+(3179+2080+9060+4160+2080+4380+4660+4160+4160)/2+12500
if __name__ == '__main__':
    fetchRent()
    # 'rentTaipei.json'
    # 'rentNewTaipei1.json'
    # 'rentNewTaipei2.json'
    # DataArrange.exec('rent.json', 'rentTaipei.xlsx', 'https://sale.591.com.tw')
    pass
