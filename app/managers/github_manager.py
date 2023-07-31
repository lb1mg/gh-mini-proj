import os
from pprint import pprint
from typing import List, Tuple

import asyncio
import aiohttp
from aiohttp_client_cache import CachedSession, SQLiteBackend, RedisBackend

from sanic import Sanic
from sanic.exceptions import NotFound, BadRequest
from sanic.log import logger

from app.cache import EfficientRedisBackend
from app.models.users import User, UserRepo, Follower, Event
from app.models.repos import Repo, Contributors, Stargazers, Comments, Commits

class GithubManager:
    """
    Base class for making async requests
    """
    
    def __init__(self) -> None:
        
        self._app:Sanic = Sanic.get_app()
        self._session:CachedSession = self._app.ctx.cached_session
        
        self._GITHUB_API_TOKEN = os.getenv("GITHUB_PAT")
        self._headers = {"Authorization": f"Bearer {self._GITHUB_API_TOKEN}"}
        
        self.timeout = aiohttp.ClientTimeout(total=60*3) # 60*3=180sec

    async def _fetch(self, url:str):
        async with self._session.get(
            url=url,
            headers=self._headers,
            timeout=self.timeout
        ) as res:
            logger.info(f"URL:{url} - Cached:{res.from_cache} - Created:{res.created_at} - Expires:{res.expires}")
            self._raise_for_status(res.status)
            result = await res.json()
            return result
        
    def _raise_for_status(self, status:int) -> None:
        if status == 400:
            raise BadRequest()
        elif status == 404:
            raise NotFound()

class UserManager(GithubManager):
    
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
    
    
class RepoManager(GithubManager):
    
    async def fetch_repo(self, ownername: str, reponame: str):
        repo_info, repo_contributors, repo_stargazers, repo_comments, repo_commits = await asyncio.gather(
            self.fetch_repo_info(ownername, reponame),
            self.fetch_repo_contributors(ownername, reponame),
            self.fetch_repo_stargazers(ownername, reponame),
            self.fetch_repo_comments(ownername, reponame),
            self.fetch_repo_commits(ownername, reponame)
        )
        return repo_info, repo_contributors, repo_stargazers, repo_comments, repo_commits
        
    async def compare_repo(self, user1:str, repo1:str, user2:str, repo2:str):
        repo1_info, repo2_info = await asyncio.gather(
            self.fetch_repo_info(user1, repo1),
            self.fetch_repo_info(user2, repo2)
        )
        return repo1_info, repo2_info
    
    async def fetch_repo_info(self, ownername: str, reponame: str):
        url = f"https://api.github.com/repos/{ownername}/{reponame}"
        result =  await self._fetch(url)
        repo = Repo(**result)
        return repo

    async def fetch_repo_contributors(self, ownername: str, reponame: str):
        url = f"https://api.github.com/repos/{ownername}/{reponame}/contributors"
        result =  await self._fetch(url)
        contributors = [Contributors(**contributor) for contributor in result]
        return contributors

    async def fetch_repo_stargazers(self, ownername: str, reponame: str):
        url = f"https://api.github.com/repos/{ownername}/{reponame}/stargazers"
        return await self._fetch(url)

    async def fetch_repo_comments(self, ownername: str, reponame: str):
        url = f"https://api.github.com/repos/{ownername}/{reponame}/comments"
        return await self._fetch(url)

    async def fetch_repo_commits(self, ownername: str, reponame: str):
        url = f"https://api.github.com/repos/{ownername}/{reponame}/commits"
        return await self._fetch(url)