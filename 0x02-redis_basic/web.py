import requests
import redis
from functools import wraps
import time

# Initialize Redis connection
redis_conn = redis.Redis()


def get_page(url: str) -> str:
    """
    Fetches the HTML content of a URL and caches
    it with an expiration of 10 seconds.

    Args:
        url (str): The URL to fetch HTML content from.

    Returns:
        str: The HTML content of the URL.
    """
    # Track access count for this URL
    count_key = f"count:{url}"
    redis_conn.incr(count_key)

    # Check if content is cached
    cached_content = redis_conn.get(url)
    if cached_content:
        return cached_content.decode('utf-8')

    # Fetch the content from the URL
    response = requests.get(url)
    if response.status_code == 200:
        html_content = response.text
        # Cache the content for 10 seconds
        redis_conn.setex(url, 10, html_content)
        return html_content
    else:
        return f"Error fetching URL: {url}. " \
               f"Status code: {response.status_code}"


def cached(func):
    """
    Decorator function to cache the result of get_page with expiration time.

    Args:
        func (Callable): The function to decorate.

    Returns:
        Callable: The decorated function.
    """
    @wraps(func)
    def wrapper(url):
        # Check if content is cached
        cached_content = redis_conn.get(url)
        if cached_content:
            return cached_content.decode('utf-8')

        # Call the original function
        html_content = func(url)
        if html_content:
            # Cache the content for 10 seconds
            redis_conn.setex(url, 10, html_content)
        return html_content:
            return wrapper


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
