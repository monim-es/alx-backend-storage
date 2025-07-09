#!/usr/bin/env python3
"""
Web caching and tracker using Redis
"""
import redis
import requests
from typing import Callable
from functools import wraps


# Connect to Redis
r = redis.Redis()


def count_url_access(method: Callable) -> Callable:
    """Decorator to count URL accesses."""
    @wraps(method)
    def wrapper(url: str) -> str:
        r.incr(f"count:{url}")
        return method(url)
    return wrapper


def cache_result(method: Callable) -> Callable:
    """Decorator to cache URL content with a 10s expiration."""
    @wraps(method)
    def wrapper(url: str) -> str:
        cached = r.get(f"cache:{url}")
        if cached:
            return cached.decode('utf-8')
        result = method(url)
        r.setex(f"cache:{url}", 10, result)
        return result
    return wrapper


@count_url_access
@cache_result
def get_page(url: str) -> str:
    """Fetch the content of a URL and cache it."""
    response = requests.get(url)
    return response.text
