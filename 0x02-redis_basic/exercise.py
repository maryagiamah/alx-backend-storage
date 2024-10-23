#!/usr/bin/env python3
"""Create a Cache class"""
import redis
import uuid
from typing import Union, Optional, Callable
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """Count calls"""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Returned Callable"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)
    return wrapper


def call_history(method: Callable) -> Callable:
    """Store history of imput and output"""
    in_list = f"{method.__qualname__}:inputs"
    out_list = f"{method.__qualname__}:outputs"

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """Returned Callable"""
        self._redis.rpush(in_list, str(args))
        output = str(method(self, *args, **kwargs))
        self._redis.rpush(out_list, output)
        return output
    return wrapper


def replay(self, fn: Callable) -> None:
    """Display the history of calls of a function"""
    redis = redis.Redis()
    in_list = redis.lrange(f"{fn.__qualname__}:inputs", 0, -1)
    out_list = redis.lrange(f"{fn.__qualname__}:outputs", 0, -1)

    print("{} was called {} times:".format(
        fn.__qualname__,
        redis.llen(f'{fn.__qualname__}:inputs')
    ))

    for in_p, out_p in zip(in_list, out_list):
        print("{fn.__qualname__}(*({in_p},)) -> {out_p}")


class Cache:
    """Cache class"""

    def __init__(self):
        """Init Class"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """Store method"""
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key

    def get(self, key: str, fn: Optional[Callable] = None) -> Union[
            str,
            bytes,
            int,
            float]:
        """Get method"""
        if fn is None:
            return self._redis.get(key)
        return fn(self._redis.get(key))

    def get_str(self, key: str) -> str:
        """Get str"""
        return self._redis.get(key, lambda k: k.decode('utf-8'))

    def get_int(self, key: str) -> int:
        """Get int"""
        return self._redis.get(key, lambda k: int(k.decode('utf-8')))
