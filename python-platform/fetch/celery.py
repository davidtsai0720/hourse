# -*- coding: utf-8 -*-
import os

from celery import Celery

BROKER = os.getenv("BROKER")

app = Celery("tasks", broker=BROKER, include=["fetch.tasks"])
app.conf.update(result_expires=3600)
