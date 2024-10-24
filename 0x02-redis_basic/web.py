#!/usr/bin/env python3
import redis
import requests
from functools import wraps
"""Implementing an expiring web cache and tracker"""

red_loc = redis.Redis()

def count_calls(method):
    """Decorator to count calls and implement caching"""
    @wraps(method)
    def wrapper(*args, **kwargs):
        """Wrap Function"""
        url = args[0]
        count_key = f"count:{url}"
        cache_key = f"cache:{url}"

        # Increment the count for this URL
        red_loc.incr(count_key)

        # Check if the URL is cached
        cache_res = red_loc.get(cache_key)
        if cache_res:
            return cache_res.decode('utf-8')

        # Fetch content and cache it
        output = method(*args, **kwargs)
        red_loc.setex(cache_key, 10, output)  # Cache for 10 seconds
        return output

    return wrapper

@count_calls
def get_page(url: str) -> str:
    """Fetch the content of a URL"""
    response = requests.get(url)
    return response.text

if __name__ == '__main__':
    url = 'http://slowwly.robertomurray.co.uk/'
    for i in range(5):
        print(get_page(url))
