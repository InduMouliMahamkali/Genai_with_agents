# caching/cache_decorator.py

from functools import wraps
from caching.cache_manager import CacheManager

cache_manager = CacheManager()

def cache_response(ttl=None):
    """
    Decorator to cache function responses in Redis using the function's arguments as key.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Build cache key based on function name and args
            query = kwargs.get('query') or (args[1] if len(args) > 1 else "")
            key = f"{func.__module__}.{func.__name__}:{query.lower().strip()}"

            # Check Redis for existing cache
            cached_result = cache_manager.get(key)
            if cached_result:
                return f"🧠 (Cached): {cached_result}"

            # Compute response and store it
            result = func(*args, **kwargs)
            cache_manager.set(key, result, ttl=ttl)
            return result
        return wrapper
    return decorator
