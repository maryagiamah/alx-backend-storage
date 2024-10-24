#!/usr/bin/env python3
"""Implementing an expiring web cache and tracker"""
import redis
import requests
from functools import wraps
from typing import Callable

red_loc = redis.Redis()


def count_calls(method: Callable) -> Callable:
    """Count calls"""
    @wraps(method)
    def wrapper(url):
        """Returned Callable"""
        count_key = f"count:{url}"
        cache_key = f"cache:{url}"

        red_loc.incr(count_key)
        cache_res = red_loc.get(cache_key)

        if cache_res:
            return cache_res.decode('utf-8')
        output = method(url)
        red_loc.setex(cache_key, 10, output)
        return output
    return wrapper


@count_calls
def get_page(url: str) -> str:
    """Track how many times a particular URL was accessed"""
    return requests.get(url).text


if __name__ == '__main__':
    get_page('http://slowwly.robertomurray.co.uk')
