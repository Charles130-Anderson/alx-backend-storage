#!/usr/bin/env python3

import requests
import redis
from functools import wraps


store = redis.Redis(host='localhost', port=6379, db=0)


def cache_and_count(func):
    """
    Decorator for caching and counting URL accesses.
    Wraps a function to cache its return value and increment
    an access counter in Redis for each unique URL argument.
    """
    @wraps(func)
    def wrapper(url: str) -> str:
        """
        Checks cache for existing content; if absent, fetches,
        caches, and counts access.
        Args:
            url (str): The URL to fetch content for.
        Returns:
            str: HTML content of the URL.
        """
        cached_key = f"cached:{url}"
        count_key = f"count:{url}"

        cached_content = store.get(cached_key)
        if cached_content:
            return cached_content.decode("utf-8")

        html_content = func(url)

        store.set(cached_key, html_content, ex=10)
        store.incr(count_key)

        return html_content

    return wrapper


@cache_and_count
def get_page(url: str) -> str:
    """
    Fetches HTML content of a given URL.
    Uses the requests library to perform a GET request to the
    specified URL and returns the HTML content.
    """
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk"
    print("First access:")
    html_content = get_page(url)
    print("Access count:", store.get(f"count:{url}").decode("utf-8"))

    print("\nSecond access (should be faster due to caching):")
    html_content = get_page(url)
    print("Access count:", store.get(f"count:{url}").decode("utf-8"))
