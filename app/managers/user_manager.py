import os
from pprint import pprint
from typing import List, Tuple

import asyncio
import aiohttp
from aiohttp import ClientSession
from aiohttp_client_cache import CachedSession, SQLiteBackend, RedisBackend

from sanic import Sanic
from sanic.exceptions import NotFound, BadRequest
from sanic.log import logger

from app.cache import EfficientRedisBackend
from app.models.users import User, UserRepo, Follower, Event
from app.models.repos import Repo, Contributors, Stargazers, Comments, Commits
from app.managers.github_manager import GithubManager

class UserManager(GithubManager):
    
    def __init__(self, token: str = None) -> None:
        super().__init__(token)
    
    async def fetch_user(self, username:str):
        user_bio, user_repos, user_events, user_followers = await asyncio.gather(
            self.fetch_user_info(username),
            self.fetch_user_repos(username),
            self.fetch_user_events(username),
            self.fetch_user_followers(username)
        )
        return user_bio, user_repos, user_events, user_followers
    
    async def compare_user(self, user1:str, user2:str) -> Tuple[User, User]:
        user1_info, user2_info = await asyncio.gather(
            self.fetch_user_info(user1),
            self.fetch_user_info(user2)
        )
        return user1_info, user2_info
        
    async def fetch_user_info(self, username: str) -> User:
        url = f"https://api.github.com/users/{username}"
        result = await self._fetch(url)
        user = User(**result)
        return user

    async def fetch_user_repos(self, username: str) -> List[UserRepo]:
        url = f"https://api.github.com/users/{username}/repos"
        result = await self._fetch(url)
        user_repos = [UserRepo(**repo) for repo in result]
        return user_repos

    async def fetch_user_events(self, username: str) -> List[Event]:
        url = f"https://api.github.com/users/{username}/events"
        result = await self._fetch(url)
        events = [Event(**event) for event in result]
        return events

    async def fetch_user_followers(self, username: str) -> List[Follower]:
        url = f"https://api.github.com/users/{username}/followers"
        result = await self._fetch(url)
        followers = [Follower(**follower) for follower in result]
        return followers