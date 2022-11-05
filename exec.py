from datetime import datetime, timedelta

from fetch.tasks import fetchShiyi


if __name__ == '__main__':
    fetchShiyi.apply_async(({
        'city': 'Taipei',
        'page': 1
    },), eta=datetime.utcnow() + timedelta(seconds=5))
