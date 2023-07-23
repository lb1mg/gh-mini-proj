import os
from pprint import pprint

import aiohttp
import asyncio
from aiohttp_client_cache import CachedSession, SQLiteBackend, RedisBackend

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('cache.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.addHandler(fh)

class Request():
    
    GITHUB_API_TOKEN = os.getenv('GITHUB_PAT')
    headers = {
        'Authorization': f'Bearer {GITHUB_API_TOKEN}'
    }
    
    @classmethod
    async def _fetch(cls, url:str):
        async with aiohttp.ClientSession(headers=cls.headers) as session:
            async with session.get(url) as res:
                result = await res.json()
                # logger.info(f'Cached:{False} Response:{result}')
                print(result)
                return result

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
    
    cache = RedisBackend(
        expire_after=60*60 # 3600 seconds
    )
    
    @classmethod
    async def _fetch(cls, url:str):
        async with CachedSession(cache=cls.cache, headers=cls.headers) as session:
            async with session.get(url) as res:
                result = await res.json()
                logger.info(f'URL:{url} - Cached:{res.from_cache} - Created at:{res.created_at} - Expires in:{res.expires} - Is expired:{res.is_expired}')
                return result

if __name__ == '__main__':
    # result = asyncio.run(CachedRequest.fetch_user('miguelgrinberg'))
    # result = asyncio.run(fetch_user_repos('miguelgrinberg'))
    # result = asyncio.run(fetch_repo('miguelgrinberg', 'microblog'))
    # result = asyncio.run(fetch_repo('google', 'leveldb'))
    # result = asyncio.run(CachedRequest.fetch_org('bloomberg'))
    # result = asyncio.run(CachedRequest.fetch_user('livewire'))
    # result = asyncio.run(Request.fetch_org('google'))
    # result = asyncio.run(fetch_org_repos('google'))
    # result = asyncio.run(Request.fetch_user('llllllllllllllll'))
    # result = asyncio.run(CachedRequest.fetch_org('facebookresearch'))
    # asyncio.run(CachedRequest._get_cached_urls())
    # print(type(result))
    # pprint(result)
    pass