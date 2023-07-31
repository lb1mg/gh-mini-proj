
import aiohttp
from aiohttp_client_cache import CachedSession, SQLiteBackend, RedisBackend

from sanic import Sanic
from sanic.log import logger

from app.cache import EfficientRedisBackend

class RequestManager:
    
    def __init__(self, session:CachedSession=None) -> None:
        self._app = Sanic.get_app()
        self._redis = self._app.ctx.redis
        self.session = session
        # self.session = CachedSession()
        pass
    
    async def make_get(self, url:str):
        pass
    
    async def make_post(self, url:str):
        pass