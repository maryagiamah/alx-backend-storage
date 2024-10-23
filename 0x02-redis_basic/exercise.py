#!/usr/bin/env python3
"""Create a Cache class"""
import redis
import uuid
from typing import Union, Optional, Callable


class Cache:
    """Cache class"""

    def __init__(self):
        """Init Class"""
        self._redis = redis.Redis()
        self._redis.flushdb()

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
