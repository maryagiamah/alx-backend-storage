#!/usr/bin/env python3
"""Implementing an expiring web cache and tracker"""
import redis
import requests
from functools import wraps
from typing import Callable

red_loc = redis.Redis()


def count_calls(method: Callable) -> Callable:
    """Decorator to count calls and implement caching"""
    @wraps(method)
    def wrapper(*args, **kwargs):
        """Wrap Function"""
        url = args[0]
        count_key = f"count:{url}"
        cache_key = f"cache:{url}"

        red_loc.incr(count_key)

        cache_res = red_loc.get(cache_key)
        if cache_res:
            return cache_res.decode('utf-8')

        output = method(*args, **kwargs)
        red_loc.setex(cache_key, 10, output)
        return output

    return wrapper


@count_calls
def get_page(url: str) -> str:
    """Fetch the content of a URL"""
    response = requests.get(url)
    return response.text


if __name__ == '__main__':
    url = 'http://slowwly.robertomurray.co.uk'
    for i in range(5):
        print(get_page(url))
