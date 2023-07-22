import os
from pprint import pprint

import aiohttp
import asyncio
from aiohttp_client_cache import CachedSession, SQLiteBackend, RedisBackend

class Request():
    
    @classmethod
    async def _fetch(cls, url:str):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as res:
                # log status here
                return await res.json()

    @classmethod
    async def fetch_user(cls, username:str):
        url = f'https://api.github.com/users/{username}'
        return await cls._fetch(url)
        
    @classmethod
    async def fetch_user_repos(cls, username:str):
        url = f'https://api.github.com/users/{username}/repos'
        return await cls._fetch(url)

    @classmethod
    async def fetch_repo(cls, ownername:str, reponame:str):
        url = f'https://api.github.com/repos/{ownername}/{reponame}'
        return await cls._fetch(url)

    @classmethod
    async def fetch_org(cls, orgname:str):
        url = f'https://api.github.com/orgs/{orgname}'
        return await cls._fetch(url)
    
    @classmethod
    async def fetch_org_repos(cls, orgname:str):
        url = f'https://api.github.com/orgs/{orgname}/repos'
        return await cls._fetch(url)

class CachedRequest(Request):
    
    cache = RedisBackend()
    
    @classmethod
    async def _fetch(cls, url:str):
        async with CachedSession(cache=cls.cache) as session:
            async with session.get(url) as res:
                # log status here
                return await res.json()

if __name__ == '__main__':
    result = asyncio.run(CachedRequest.fetch_user('miguelgrinberg'))
    # result = asyncio.run(fetch_user_repos('miguelgrinberg'))
    # result = asyncio.run(fetch_repo('miguelgrinberg', 'microblog'))
    # result = asyncio.run(fetch_repo('google', 'leveldb'))
    # result = asyncio.run(fetch_org('google'))
    # result = asyncio.run(fetch_org_repos('google'))
    # print(type(result))
    pprint(result)