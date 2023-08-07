
"""
REDIS LISTENERS
"""
import redis.asyncio as redis

from aiohttp_client_cache import CachedSession

from sanic import Sanic
from sanic.log import logger

from app.cache import EfficientRedisBackend

async def connect_redis(app:Sanic):
    """ listener for connecting to Redis """
    app.ctx.redis = None
    _redis = redis.Redis()
    try:
        await _redis.ping()
    except Exception as e:
        logger.error(e)
        logger.error("<<<<< Could not connect to Redis! Shutting Down! >>>>>")
        app.stop()
    else:
        app.ctx.redis = _redis
        logger.info(f'<<<<< Connected to Redis >>>>>')
        
async def disconnect_redis(app:Sanic):
    """ listener to close connection to Redis """
    # await app.ctx.redis.close()
    _redis = app.ctx.redis
    if _redis:
        await _redis.close()
    logger.info(f'<<<<< Disconnected from Redis >>>>>')
    