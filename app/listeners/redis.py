
"""
REDIS LISTENERS
"""
import redis.asyncio as redis

from aiohttp_client_cache import CachedSession

from sanic import Sanic
from sanic.log import logger

from app.cache import EfficientRedisBackend

from .base import BaseListener

class RedisListener(BaseListener):
    
    @classmethod
    async def connect(cls, app):
        app.ctx.redis = None
        r = redis.Redis()
        try:
            await r.ping()
        except redis.ConnectionError as e:
            logger.error(e)
            logger.error("<<<<< Could not connect to Redis! Shutting Down! >>>>>")
            app.stop()
        else:
            app.ctx.redis = r
            logger.info(f'<<<<< Connected to Redis >>>>>')
            
    @classmethod
    async def disconnect(cls, app):
        r = app.ctx.redis
        if r:
            await r.close()
            logger.info(f'<<<<< Disconnected from Redis >>>>>')