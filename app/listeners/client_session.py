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

async def create_client_session(app:Sanic):
    app.ctx.client_session = None
    _session = aiohttp.ClientSession()
    app.ctx.client_session = _session
    logger.info('<<<<< Created Persistent Client Session >>>>>')
    
    
async def close_client_session(app:Sanic):
    _session = app.ctx.client_session
    if _session:
        await asyncio.sleep(0)
        await _session.close()
    logger.info('<<<<< Closed Persistent Client Session >>>>>')