#!/usr/bin/env python3
'''A module to fetch and cache web pages.
'''

import redis
import requests
from functools import wraps
from typing import Callable

# Initialize Redis connection
redis_instance = redis.Redis()


def cache_data(method: Callable) -> Callable:
    '''Decorator to cache fetched data's output.
    '''
    @wraps(method)
    def wrapper(url: str) -> str:
        '''Wrapper function to cache the output of data fetching.
        '''
        # Increment the access count for the URL
        count_key = f'count:{url}'
        redis_instance.incr(count_key)
        # Check if the result is already cached
        cache_key = f'result:{url}'
        cached_result = redis_instance.get(cache_key)
        if cached_result:
            return cached_result.decode('utf-8')
        # Call the original method to fetch the data
        result = method(url)
        # Cache the result with an expiration time of 10 seconds
        redis_instance.setex(cache_key, 10, result)
        return result

    return wrapper


@cache_data
def get_page(url: str) -> str:
    '''Fetches the HTML content of a URL and caches it with an expiration
    of 10 seconds.

    Args:
        url (str): The URL to fetch HTML content from.

    Returns:
        str: The HTML content of the URL.
    '''
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return (f"Error fetching URL: {url}. "
                f"Status code: {response.status_code}")


if __name__ == "__main__":
    # Test with a slow loading URL (simulated)
    test_url = ('http://slowwly.robertomurray.co.uk/delay/5000/'
                'url/http://www.example.com')
    content = get_page(test_url)
    print(f"Content of {test_url}:")
    print(content)

    # Test with a cached URL (should load faster on subsequent access within
    # 10 seconds)
    cached_content = get_page(test_url)
    print(f"Content of cached {test_url}:")
    print(cached_content)
