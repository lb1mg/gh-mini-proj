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

"""
before server start
"""
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
    
async def create_client_session(app:Sanic):
    app.ctx.client_session = None
    _session = aiohttp.ClientSession()
    app.ctx.client_session = _session
    logger.info('<<<<< Created Persistent Client Session >>>>>')

"""
before server stop
"""
async def disconnect_redis(app:Sanic):
    """ listener to close connection to Redis """
    # await app.ctx.redis.close()
    _redis = app.ctx.redis
    if _redis:
        await _redis.close()
    logger.info(f'<<<<< Disconnected from Redis >>>>>')
    
async def close_cached_session(app:Sanic):
    _session = app.ctx.cached_session
    if _session:
        await asyncio.sleep(0)
        await _session.close()
    logger.info('<<<<< Closed Persistent Cached Session >>>>>')
    
async def close_client_session(app:Sanic):
    _session = app.ctx.client_session
    if _session:
        await asyncio.sleep(0)
        await _session.close()
    logger.info('<<<<< Closed Persistent Client Session >>>>>')