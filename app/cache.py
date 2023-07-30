from typing import Any
from redis.asyncio import Redis

from aiohttp_client_cache.backends.base import BaseCache, CacheBackend
from aiohttp_client_cache.backends.redis import RedisCache

class EfficientRedisBackend(CacheBackend):
    """ Custom Cache Backend that accepts Redis connection Object """
    def __init__(self, connection:Redis, cache_name: str = 'x-aiohttp-cache', **kwargs:Any):
        super().__init__(**kwargs)
        self.responses = RedisCache(cache_name, 'responses', connection=connection, **kwargs)
        self.redirects = RedisCache(cache_name, 'redirects', connection=connection, **kwargs)
