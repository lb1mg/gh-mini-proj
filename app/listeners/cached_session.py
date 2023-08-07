"""
LISTENERS
"""
import redis.asyncio as redis

import asyncio
import aiohttp
from aiohttp_client_cache import CachedSession

from sanic import Sanic
from sanic.log import logger

from app.cache import EfficientRedisBackend

async def create_cached_session(app:Sanic):
    """ listener to create a persistent CachedSession """
    app.ctx.cached_session = None
    _redis = app.ctx.redis
    _cache_backend = EfficientRedisBackend(
        connection = _redis,
        expire_after = 60 * 60
    )
    _session = CachedSession(
        cache=_cache_backend
    )
    app.ctx.cached_session = _session
    logger.info('<<<<< Created Persistent Cached Session >>>>>')
    
async def close_cached_session(app:Sanic):
    _session = app.ctx.cached_session
    if _session:
        await asyncio.sleep(0)
        await _session.close()
    logger.info('<<<<< Closed Persistent Cached Session >>>>>')