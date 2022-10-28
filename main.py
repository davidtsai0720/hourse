#! ./venv/bin/python3.11
# -*- coding: utf-8 -*-
import json
from collections import defaultdict
from numpy import maximum

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver import FirefoxOptions
import pandas

from house import rent


def get_rent(name='/usr/bin/geckodriver') -> None:
    opts = FirefoxOptions()
    opts.headless = True
    service = Service(name)
    driver = webdriver.Firefox(service=service, options=opts)
    rents = rent.Rent(driver=driver)
    rents.run()
    driver.close()
    driver.quit()


def get_candidates(name='rent.json') -> pandas.DataFrame:
    with open(name, 'r') as f:
        out = json.loads(f.read())

    memory = set()
    array = []
    for data in out:
        key = (data['Address'], data['Price'])
        if key in memory:
            continue

        if data['Floor'] != '':

            current, maximum = data['Floor'].split('/')
            if current == maximum:
                continue

            if current[0] in ('1', '2'):
                continue

            if not current[0].isdigit():
                continue

            if data['Type'] == '公寓' and current[0] > '3':
                continue

        if data['MainArea'] == '':
            continue

        if float(data['MainArea'][2:-1]) < 23:
            continue

        if int(data['Age'][:-1]) > 40:
            continue

        data['Link'] = 'https://sale.591.com.tw' + data['Link']

        memory.add(key)
        array.append(data)
    return pandas.DataFrame(array)


def to_xlsx(candidates: pandas.DataFrame, name='output.xlsx'):
    output = pandas.DataFrame()
    for candidate in candidates.groupby(['Location', 'Age', 'Type']):
        df = candidate[1].sort_values(by=['MainArea'])
        output = pandas.concat([output, df])
    output.to_excel(name)


# 2000+11500+2655+(3179+2080+9060+4160+2080+4380+4660+4160+4160)/2+12500
if __name__ == '__main__':
    get_rent()
    # candidates = get_candidates()
    # to_xlsx(candidates)
