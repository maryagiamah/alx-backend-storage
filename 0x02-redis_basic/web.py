#!/usr/bin/env python3
import redis
import requests
from functools import wraps
from typing import Callable
"""Implementing an expiring web cache and tracker"""


def count_calls(method: Callable) -> Callable:
    """Count calls"""
    red_loc = redis.Redis()

    @wraps(method)
    def wrapper(*args, **kwargs):
        """Returned Callable"""
        key = f"count:{args[0]}"
        red_loc.incr(key)
        cache_res = red_loc.get(f"cache:{args[0]}")

        if cache_res:
            return cache_res.decode('utf-8')
        output = method(*args, **kwargs)
        red_loc.setex(f"cache:{args[0]}", 10, output)
        return output

    return wrapper


@count_calls
def get_page(url: str) -> str:
    """Track how many times a particular URL was accessed"""
    return requests.get(url).text  # Fix 'requests' spelling
