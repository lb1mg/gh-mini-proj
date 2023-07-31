
import aiohttp
from aiohttp_client_cache import CachedSession, SQLiteBackend, RedisBackend

from sanic import Sanic
from sanic.log import logger
from sanic.exceptions import NotFound, BadRequest

from app.cache import EfficientRedisBackend

class RequestManager:
    
    def __init__(self, session, headers:dict=None, timeout_total:int=None) -> None:
        self._session = session
        self._headers = headers
        # Request Config
        self._timeout_total = timeout_total
        if not self._timeout_total:
            self._timeout_total = 60*3 # 60*3=180sec
        self.timeout = aiohttp.ClientTimeout(total=self._timeout_total) 
    
    async def _fetch(self, url:str):
        async with self._session.get(
            url=url,
            headers=self._headers,
            timeout=self.timeout
        ) as res:
            # logger.info(f"URL:{url} - Cached:{res.from_cache} - Created:{res.created_at} - Expires:{res.expires}")
            self._raise_for_status(res.status)
            result = await res.json()
            return result
    
    async def _make_post(self, url:str, payload:dict):
        async with self._session.post(
            url=url,
            data=payload,
            headers=self.headers,
            timeout=self.timeout
        ) as res:
            # log
            self._raise_for_status(res.status)
            result = await res.json()
            return result
        
    def _raise_for_status(self, status:int) -> None:
        if status == 400:
            raise BadRequest()
        elif status == 404:
            raise NotFound()