#! ./venv/bin/python3.11
from celery import Celery


app = Celery(
    'tasks',
    broker='pyamqp://rabbitmq:rabbitmq@localhost/vhost',
    include=['fetch.tasks']
)


app.conf.update(result_expires=3600)
