#! ./venv/bin/python3.11
from datetime import datetime, timedelta
import logging

from .celery import app
from .upsert import Upsert
from .parse import Sinyi, Result
from .webdriver import Webdriver


@app.task
def insert(data: dict):
    try:
        Upsert(data=data)
    except Exception as e:
        logging.error(e)


@app.task
def fetch591(data: dict):
    return None


@app.task
def fetchShiyi(data: dict):
    city = data['city']
    page = data['page']
    obj = Sinyi(city=city, page=page)
    try:
        result: Result = obj.exec(driver=Webdriver)
        logging.warning(f'\ncity\t{city}\ncurrent\t{result.Page}\ntotal count\t{result.Total}\n')
        if result.Page < 3:
            fetchShiyi.apply_async(
                ({'city': city, 'page': page + 1},),
                eta=datetime.utcnow() + timedelta(seconds=5))
    except Exception as e:
        logging.error(e)


@app.task
def fetchYungChing(data: dict):
    return None
