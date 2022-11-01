#! ./venv/bin/python3.11
# -*- coding: utf-8 -*-
from enum import Enum
import logging

from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver import FirefoxOptions

from crawler import sale591, yungching, agent, sinyi

options = FirefoxOptions()
options.headless = True


class Setting(Enum):

    driverPath = '/usr/bin/geckodriver'


class Logging(Enum):

    level = logging.INFO
    format = '%(asctime)s - %(levelname)s - %(message)s'
    datefmt = '%Y-%m-%d %H:%M:%S'
    filename = 'mylog.log'


logging.basicConfig(
    filename=Logging.filename.value,
    level=Logging.level.value,
    format=Logging.format.value,
    datefmt=Logging.datefmt.value)


def exec_crawler() -> None:
    service = Service(Setting.driverPath.value)
    driver = webdriver.Firefox(service=service, options=options)
    try:
        sale = sale591.Sale591(driver=driver)
        for param in sale591.Query:
            sale.run(param.value)

        yc = yungching.YungChing(driver=driver)
        for param in agent.QueryParameter:
            yc.run(param.value)

        sy = sinyi.Sinyi(driver=driver)
        for param in agent.QueryParameter:
            sy.run(param.value)

    except Exception as e:
        logging.error(e)

    finally:
        driver.close()
        driver.quit()


if __name__ == '__main__':
    exec_crawler()
