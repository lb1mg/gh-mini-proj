import os
from pprint import pprint
from typing import List

import aiohttp
from aiohttp_client_cache import CachedSession, SQLiteBackend, RedisBackend

from sanic.exceptions import NotFound, BadRequest
from sanic.log import logger

from app.models.users import User, UserRepo, Follower, Event
from app.mylogging import logger

class Request():
    """
    Base class for making async requests 
    """
    
    GITHUB_API_TOKEN = os.getenv('GITHUB_PAT')
    headers = {
        'Authorization': f'Bearer {GITHUB_API_TOKEN}'
    }
    
    @classmethod
    async def _fetch(cls, url:str):
        async with aiohttp.ClientSession(headers=cls.headers) as session:
            async with session.get(url) as res:
                if res.status==400:
                    raise BadRequest()
                elif res.status==404:
                    raise NotFound()
                result = await res.json()
                return result

    @classmethod
    async def fetch_user(cls, username:str) -> User:
        """Fetch github user info

        Args:
            username (str): github user's username

        Returns:
            User: Pydantics User Model
        """
        url = f'https://api.github.com/users/{username}'
        result = await cls._fetch(url)
        user = User(**result)
        return user
        
    @classmethod
    async def fetch_user_repos(cls, username:str) -> List[UserRepo]:
        url = f'https://api.github.com/users/{username}/repos'
        result = await cls._fetch(url)
        user_repos = [UserRepo(**repo) for repo in result]
        return user_repos
    
    @classmethod
    async def fetch_user_events(cls, username:str) -> List[Event]:
        url = f'https://api.github.com/users/{username}/events'
        result = await cls._fetch(url)
        events = [Event(**event) for event in result]
        return events
    
    @classmethod
    async def fetch_user_followers(cls, username:str) -> List[Follower]:
        url = f'https://api.github.com/users/{username}/followers?per_page=50'
        result = await cls._fetch(url)
        followers = [Follower(**follower) for follower in result]
        return followers

    @classmethod
    async def fetch_repo(cls, ownername:str, reponame:str):
        url = f'https://api.github.com/repos/{ownername}/{reponame}'
        return await cls._fetch(url)
   
    @classmethod
    async def fetch_repo_contributors(cls, ownername:str, reponame:str):
        url = f'https://api.github.com/repos/{ownername}/{reponame}/contributors'
        return await cls._fetch(url)
     
    @classmethod
    async def fetch_repo_stargazers(cls, ownername:str, reponame:str):
        url = f'https://api.github.com/repos/{ownername}/{reponame}/stargazers'
        return await cls._fetch(url)
    
    @classmethod
    async def fetch_repo_comments(cls, ownername:str, reponame:str):
        url = f'https://api.github.com/repos/{ownername}/{reponame}/comments'
        return await cls._fetch(url)
    
    @classmethod
    async def fetch_repo_commits(cls, ownername:str, reponame:str):
        url = f'https://api.github.com/repos/{ownername}/{reponame}/commits'
        return await cls._fetch(url)

class CachedRequest(Request):
    """ 
    Extends base Request class to cache api responses 
    """
    
    cache = RedisBackend(
        expire_after=60*60 # 3600 seconds
    )
    
    @classmethod
    async def _fetch(cls, url:str):
        async with CachedSession(cache=cls.cache, headers=cls.headers) as session:
            async with session.get(url) as res:
                if res.status==400:
                    raise BadRequest()
                elif res.status==404:
                    raise NotFound()
                
                result = await res.json()
                logger.info(f'URL:{url} - Cached:{res.from_cache} - Created at:{res.created_at} - Expires in:{res.expires} - Is expired:{res.is_expired}')
                return result
