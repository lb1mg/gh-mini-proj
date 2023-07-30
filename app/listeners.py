"""
LISTENERS
"""
from sanic import Sanic
from sanic.log import logger

import redis.asyncio as redis

"""
before server start
"""
async def connect_redis(app:Sanic):
    """ istener for connecting to Redis """
    # app.ctx.redis = redis.Redis()
    app.ctx.redis = redis.from_url('redis://localhost')
    logger.info(f'<<<<< Connected to Redis >>>>>')

"""
before server stop
"""
async def disconnect_redis(app:Sanic):
    """ listener to close connection to Redis """
    await app.ctx.redis.close()
    logger.info(f'<<<<< Disconnected from Redis >>>>>')