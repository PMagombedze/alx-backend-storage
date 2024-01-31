#!/usr/bin/env python3


"""
web
"""


import requests
import redis


def get_page(url: str) -> str:
    """get page"""
    r = redis.Redis()
    cached_data = r.get(url)
    if cached_data is not None:
        r.incr(f"count:{url}")
        return cached_data.decode()

    response = requests.get(url)
    html_content = response.text
    r.setex(url, 10, html_content)
    r.set(f"count:{url}", 1)

    return html_content

print(get_page('http://slowwly.robertomurray.co.uk'))