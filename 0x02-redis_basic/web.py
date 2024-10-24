#!/usr/bin/env python3
"""Implementing an expiring web cache and tracker"""
import redis
import requests
from functools import wraps
from typing import Callable

red_loc = redis.Redis()


def count_calls(method):
    """Decorator to count calls and implement caching"""
    @wraps(method)
    def wrapper(url):
        """Wrap Function"""
        count_key = f"count:{url}"
        cache_key = f"cached:{url}"

        cache_res = red_loc.get(cache_key)
        if cache_res:
            return cache_res.decode('utf-8')

        red_loc.incr(count_key)
        output = method(url)
        red_loc.setex(cache_key, 10, output)
        return output

    return wrapper


@count_calls
def get_page(url: str) -> str:
    """Fetch the content of a URL"""
    response = requests.get(url)
    return response.text
