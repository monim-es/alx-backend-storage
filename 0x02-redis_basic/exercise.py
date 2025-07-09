#!/usr/bin/env python3
"""
Module for Redis-based cache
"""
import redis
import uuid
from typing import Union


class Cache:
    def __init__(self):
        """Initialize the Redis client and flush the DB."""
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the data in Redis using a random key.

        Args:
            data: Data to store (str, bytes, int, or float).

        Returns:
            The key under which the data is stored.
        """
        key = str(uuid.uuid4())
        self._redis.set(key, data)
        return key
