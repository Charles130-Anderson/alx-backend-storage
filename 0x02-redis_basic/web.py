#!/usr/bin/env python3
'''Provides tools for caching and tracking HTTP requests.
'''
import redis
import requests
from functools import wraps
from typing import Callable

# Redis instance for caching
redis_instance = redis.Redis()
'''The Redis instance used for caching.
'''


def cache_data(method: Callable) -> Callable:
    '''Decorator to cache fetched data's output.
    '''
    @wraps(method)
    def wrapper(url) -> str:
        '''Wrapper function to cache the output of data fetching.
        '''
        redis_instance.incr(f'count:{url}')
        result = redis_instance.get(f'result:{url}')
        if result:
            return result.decode('utf-8')
        result = method(url)
        redis_instance.set(f'count:{url}', 0)
        redis_instance.setex(f'result:{url}', 10, result)
        return result
    return wrapper


@cache_data
def get_page(url: str) -> str:
    '''Fetches the content of a URL, caches the response,
    and tracks the request.
    '''
    return requests.get(url).text


# Example usage:
if __name__ == "__main__":
    # Test with a slow loading URL (simulated)
    url = 'http://slowwly.robertomurray.co.uk/delay/5000/' \
          'url/http://www.example.com'
    content = get_page(url)
    print(f"Content of {url}:")
    print(content)

    content_cached = get_page(url)
    print(f"Content of cached {url}:")
    print(content_cached)
