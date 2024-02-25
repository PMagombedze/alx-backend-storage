#!/usr/bin/env python3

import redis
import uuid
from typing import Union, Callable
from functools import wraps


class Cache:
    def __init__(self):
        """
        Initializes the Cache class with a Redis client instance
        """
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores the input data in Redis using a random key and returns the key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None):
        """
        Retrieves data from Redis using the provided key
        """
        value = self._redis.get(key)
        if value is None:
            return None
        return fn(value) if fn else value

    def get_str(self, key: str) -> Union[str, None]:
        """
        Retrieves data from Redis as a UTF-8 string
        """
        return self.get(key, fn=lambda d: d.decode("utf-8"))

    def get_int(self, key: str) -> Union[int, None]:
        """
        Retrieves data from Redis as an integer
        """
        return self.get(key, fn=int)

    @staticmethod
    def count_calls(method: Callable) -> Callable:
        """
        Decorator to count the number of times a method is called
        """
        @wraps(method)
        def wrapper(self, *args, **kwargs):
            key = f"calls:{method.__qualname__}"
            self._redis.incr(key)
            return method(self, *args, **kwargs)
        return wrapper

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Stores the input data in Redis using a random key and returns the key
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
