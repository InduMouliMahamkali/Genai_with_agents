import redis
import os
import hashlib
import json
import time

class CacheManager:
    def __init__(self, host='localhost', port=6380, db=0, ttl_seconds=3600):
        self.redis = redis.StrictRedis(
            host=os.getenv("REDIS_HOST", host),
            port=int(os.getenv("REDIS_PORT", port)),
            db=int(os.getenv("REDIS_DB", db)),
            decode_responses=True
        )
        self.ttl_seconds = ttl_seconds

    def _make_key(self, query: str, prefix: str = "cache:") -> str:
        hashed = hashlib.sha256(query.encode()).hexdigest()
        return f"{prefix}{hashed}"

    def get(self, query: str) -> str:
        key = self._make_key(query)
        return self.redis.get(key)

    def set(self, query: str, response: str, ttl: int = None):
        key = self._make_key(query)
        ttl_to_use = ttl if ttl is not None else self.ttl_seconds
        self.redis.setex(key, ttl_to_use, response)

    def invalidate(self, query: str):
        key = self._make_key(query)
        self.redis.delete(key)

    def flush_all(self):
        self.redis.flushdb()

    def exists(self, query: str) -> bool:
        key = self._make_key(query)
        return self.redis.exists(key) == 1
