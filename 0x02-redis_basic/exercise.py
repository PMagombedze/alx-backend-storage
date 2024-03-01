#!/usr/bin/env python3

"""Redis"""

import uuid
from typing import Callable, Union
from functools import wraps
import redis


def count_calls(method: Callable) -> Callable:
    """count calls"""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """call history"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """wrapper"""
        keyIn = method.__qualname__ + ":inputs"
        keyOut = method.__qualname__ + ":outputs"

        output = method(self, *args, **kwargs)

        self._redis.rpush(keyIn, str(args))
        self._redis.rpush(keyOut, str(output))

        return output

    return wrapper


def replay(fn: Callable):
    """replay"""
    r = redis.Redis()
    name = fn.__qualname__
    calls = r.get(name)
    try:
        calls = calls.decode('utf-8')
    except Exception:
        calls = 0
    print(f'{name} was called {calls} times:')
    outs = r.lrange(name + ":outputs", 0, -1)
    ins = r.lrange(name + ":inputs", 0, -1)
    for i, j in zip(ins, outs):
        try:
            i = i.decode('utf-8')
        except Exception:
            i = ""
        try:
            j = j.decode('utf-8')
        except Exception:
            j = ""
        print(f'{name}(*{i}) -> {j}')


class Cache():
    """Cache"""
    def __init__(self) -> None:
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store method"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Callable = None)\
            -> Union[str, bytes, int, float]:
        """Get data from redis"""
        data = self._redis.get(key)
        if fn:
            return fn(data)
        return data

    def get_str(self, key: str) -> str:
        """get string"""
        var = self._redis.get(key)
        return var.decode("UTF-8")

    def get_int(self, key: str) -> int:
        """get integer"""
        var = self._redis.get(key)
        try:
            var = int(var.decode("UTF-8"))
        except Exception:
            var = 0
        return var
