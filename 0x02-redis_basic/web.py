#!/usr/bin/env python3


"""
web cacher and tracker
"""


import redis
import requests
from functools import wraps

r = redis.Redis()


def URL(method):
    """url access count"""
    @wraps(method)
    def wrapper(url):
        """wrapper function"""
        key = "cached:" + url
        cache = r.get(key)
        if cache:
            return cache.decode("utf-8")

        count = "count:" + url
        content = method(url)

        r.incr(count)
        r.set(key, content, ex=10)
        r.expire(key, 10)
        return content
    return wrapper


@URL
def get_page(url: str) -> str:
    """obtain the HTML content"""
    results = requests.get(url)
    return results.text


if __name__ == "__main__":
    get_page('http://slowwly.robertomurray.co.uk')
