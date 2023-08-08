import json

import aiohttp
from aiohttp_client_cache import CachedSession, SQLiteBackend, RedisBackend

from sanic import Sanic
from sanic.log import logger
from sanic.exceptions import NotFound, BadRequest

from app.cache import EfficientRedisBackend

class RequestManagerV2:
    
    @classmethod
    async def _get_session(cls, cache:bool = False):
        app = Sanic.get_app()
        if cache:
            return app.ctx.cached_session
        return app.ctx.client_session
    
    @classmethod
    async def _request(
        cls,
        method:str, 
        url:str,
        headers:dict = None,
        params:dict = None,
        data:dict = None,
        cache:bool = False, 
        raise_for_status:bool = True
    ):
        if not headers:
            # TODO: pick from config
            pass
        
        timeout_total = 120 # TODO:pick from config
        timeout = aiohttp.ClientTimeout(total=timeout_total) 
        
        data = json.dumps(data)
        
        session = cls._get_session(cache=cache)
        
        async with session.request(
            method = method,
            url = url,
            headers = headers,
            params = params,
            data = data,
            timeout=timeout,
            raise_for_status=raise_for_status
        ) as resp:
            if cache:
                logger.info(f"URL:{url} - Cached:{resp.from_cache} - Created:{resp.created_at} - Expires:{resp.expires}")
            result = await resp.json()
            return result
                
    @classmethod
    async def _fetch(
        cls,
        method:str, 
        url:str,
        headers:dict = None,
        params:dict = None,
        data:dict = None,
        cache:bool = False, 
        raise_for_status:bool = True
    ):
        result = await cls._request(
            method = "GET",
            url = url,
            headers = headers,
            params = params,
            data = data,
            cache=cache,
            raise_for_status=raise_for_status,
        )
        return result
    
    # TODO: _make_post
    # TODO: _make_put
    # TODO: _make_delete


class RequestManager:
    
    def __init__(self, cache:bool=True, headers:dict=None, timeout_total:int=180) -> None:
        # get current running sanic instance
        self._app = Sanic.get_app()
        # set session acc to cache param
        self._session = None
        self._to_cache = cache
        if cache:
            self._session = self._app.ctx.cached_session
        else:
            self._session = self._app.ctx.client_session
        # set headers
        self._headers = headers
        # Request Config
        self._timeout_total = timeout_total
        self.timeout = aiohttp.ClientTimeout(total=self._timeout_total) 
    
    async def _fetch(self, url:str):
        """Makes a GET request & fetches data

        Args:
            url (str): url to send request  
        Returns:
            dict: response dictionary
        """
        async with self._session.get(
            url=url,
            headers=self._headers,
            timeout=self.timeout,
            raise_for_status=True
        ) as res:
            if self._to_cache:
                logger.info(f"URL:{url} - Cached:{res.from_cache} - Created:{res.created_at} - Expires:{res.expires}")
            # self._raise_for_status(res.status)
            result = await res.json()
            return result
    
    async def _make_post(self, url:str, payload:dict):
        async with self._session.post(
            url=url,
            data=payload,
            headers=self._headers,
            timeout=self.timeout
        ) as res:
            # log
            self._raise_for_status(res.status)
            result = await res.json()
            return result
        
    async def _make_delete(self, url:str):
        async with self._session.delete(
            url=url
        ) as res:
            self._raise_for_status(res.status)
            result = await res.json()
            return result
        
    def _raise_for_status(self, status:int) -> None:
        if status == 400:
            raise BadRequest()
        elif status == 404:
            raise NotFound()