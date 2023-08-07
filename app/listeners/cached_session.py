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

from .base import BaseListener

class CachedSessionListener(BaseListener):
    
    @classmethod
    async def connect(cls, app):
        app.ctx.cached_session = None
        r = app.ctx.redis
        cache_backend = EfficientRedisBackend(
            connection = r,
            expire_after = 60 * 60
        )
        session = CachedSession(
            cache=cache_backend
        )
        app.ctx.cached_session = session
        logger.info('<<<<< Created Persistent Cached Session >>>>>')
        
    @classmethod
    async def disconnect(cls, app):
        session = app.ctx.cached_session
        if session:
            await asyncio.sleep(0)
            await session.close()
            logger.info('<<<<< Closed Persistent Cached Session >>>>>')
