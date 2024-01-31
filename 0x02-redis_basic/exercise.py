#!/usr/bin/env python3


"""
exercise
"""


import redis
import uuid
from typing import Any


class Cache:
    def __init__(self):
        """initialization"""
        self.__redis = redis.Redis()
        self.__redis.flushdb()

    def store(self, data: Any) -> str:
        """returns random key"""
        randomKey = uuid.uuid4()
        self.__redis.set(str(randomKey), data)
        return str(randomKey)
