# -*- coding: utf-8 -*-
from typing import NamedTuple
from collections.abc import Iterator

Result = NamedTuple("Result", [("body", Iterator[dict]), ("has_next", bool)])
Node = NamedTuple("Node", [("tag", str), ("class_name", str)])
