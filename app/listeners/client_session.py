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

class ClientSessionListener(BaseListener):
    
    @classmethod
    async def connect(cls, app):
        app.ctx.client_session = None
        session = aiohttp.ClientSession()
        app.ctx.client_session = session
        logger.info('<<<<< Created Persistent Client Session >>>>>')
        
    @classmethod
    async def disconnect(cls, app):
        session = app.ctx.client_session
        if session:
            await asyncio.sleep(0)
            await session.close()
        logger.info('<<<<< Closed Persistent Client Session >>>>>')