# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from fetch import upsert_hourse

upsert_hourse.apply_async((0, 0, 1), eta=datetime.utcnow() + timedelta(seconds=1))
