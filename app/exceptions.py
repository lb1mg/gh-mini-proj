"""
EXCEPTIONS
"""
from redis import ConnectionError

from sanic.log import logger
from sanic.response import json

def redis_conn_err_handler(request, exception):
    logger.info('redis conn error!')
    return json({'msg': 'redis phatt gya!'})

def pydantic_val_err_handler(request, exceptions):
    logger.info('pydantic validation error!')
    return json({'msg': 'not yo type my man!'})