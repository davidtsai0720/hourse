#! ./venv/bin/python3.11
from datetime import datetime, timedelta
from fetch.tasks import fetchShiyi
# import time

if __name__ == '__main__':
    fetchShiyi.apply_async(({
        'city': 'Taipei',
        'page': 1
    },), eta=datetime.utcnow() + timedelta(seconds=5))
