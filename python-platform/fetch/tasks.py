# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
import logging

from .celery import app
from .upsert import handle_upsert_hourse
from .parse import Sinyi, Result
from .webdriver import Webdriver
from .settings import Settings


@app.task
def upsert_rds(body: dict) -> str:
    try:
        return handle_upsert_hourse(data=body)
    except Exception as e:
        logging.error(e)
        return e


@app.task
def upsert_hourse(city_num: int, page: int):
    city = Settings.Cities.value[city_num]
    obj = Sinyi(city=city, page=page)
    try:
        result: Result = obj.exec(driver=Webdriver)
        params = (city_num, page + 1) if result.has_next else ((city_num + 1) % len(Settings.Cities.value), 1)
        upsert_hourse.apply_async(args=params, eta=datetime.utcnow() + timedelta(seconds=5))

        for body in result.body:
            upsert_rds.apply_async(args=(body,), eta=datetime.utcnow())

    except Exception as e:
        logging.error(e)

    return f'city:{city}\tpage:{page}\tdone'
