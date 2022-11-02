#! ./venv/bin/python3.11
# -*- coding: utf-8 -*-
from enum import Enum
import logging

from crawler import sale591, yungching, agent, sinyi


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
    try:
        sale = sale591.Sale591()
        for param in sale591.Query:
            sale.run(param.value)

        yc = yungching.YungChing()
        for param in agent.QueryParameter:
            yc.run(param.value)

        sy = sinyi.Sinyi()
        for param in agent.QueryParameter:
            sy.run(param.value)

    except Exception as e:
        logging.error(e)


if __name__ == '__main__':
    exec_crawler()
