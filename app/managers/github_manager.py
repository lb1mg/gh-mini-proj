import os
from pprint import pprint
from typing import List


import aiohttp
from aiohttp_client_cache import CachedSession, SQLiteBackend, RedisBackend

from sanic.exceptions import NotFound, BadRequest

from app.models.users import User, UserRepo, Follower, Event
from app.models.repos import Repo, Contributors, Stargazers, Comments, Commits

from app.logger import logger


class GithubManager:
    """
    Base class for making async requests
    """

    GITHUB_API_TOKEN = os.getenv("GITHUB_PAT")
    headers = {"Authorization": f"Bearer {GITHUB_API_TOKEN}"}

    @classmethod
    async def _fetch(cls, url: str) -> dict:
        """Makes a GET request & fetches data

        Args:
            url (str): url to send request  
        Returns:
            dict: response dictionary
        """
        async with aiohttp.ClientSession(headers=cls.headers) as session:
            async with session.get(url) as res:
                if res.status == 400:
                    raise BadRequest()
                elif res.status == 404:
                    raise NotFound()
                result = await res.json()
                return result

    @classmethod
    async def fetch_user(cls, username: str) -> User:
        """Fetch github user info

        Args:
            username (str): github username

        Returns:
            User: User object
        """
        url = f"https://api.github.com/users/{username}"
        result = await cls._fetch(url)
        user = User(**result)
        return user

    @classmethod
    async def fetch_user_repos(cls, username: str) -> List[UserRepo]:
        """Fetch github user repos

        Args:
            username (str): github username

        Returns:
            List[UserRepo]: A list of UserRepo objects
        """
        url = f"https://api.github.com/users/{username}/repos"
        result = await cls._fetch(url)
        user_repos = [UserRepo(**repo) for repo in result]
        return user_repos

    @classmethod
    async def fetch_user_events(cls, username: str) -> List[Event]:
        """Fetch user's github event

        Args:
            username (str): github username

        Returns:
            List[Event]: A list of Event objects
        """
        url = f"https://api.github.com/users/{username}/events"
        result = await cls._fetch(url)
        events = [Event(**event) for event in result]
        return events

    @classmethod
    async def fetch_user_followers(cls, username: str) -> List[Follower]:
        """Fetch user followers

        Args:
            username (str): github username

        Returns:
            List[Follower]: A list of Follower objectss
        """
        url = f"https://api.github.com/users/{username}/followers?per_page=50"
        result = await cls._fetch(url)
        followers = [Follower(**follower) for follower in result]
        return followers

    @classmethod
    async def fetch_repo(cls, ownername: str, reponame: str):
        
        url = f"https://api.github.com/repos/{ownername}/{reponame}"
        result =  await cls._fetch(url)
        repo = Repo(**result)
        return repo

    @classmethod
    async def fetch_repo_contributors(cls, ownername: str, reponame: str):
        url = f"https://api.github.com/repos/{ownername}/{reponame}/contributors"
        result =  await cls._fetch(url)
        contributors = [Contributors(**contributor) for contributor in result]
        return contributors

    @classmethod
    async def fetch_repo_stargazers(cls, ownername: str, reponame: str):
        url = f"https://api.github.com/repos/{ownername}/{reponame}/stargazers"
        return await cls._fetch(url)

    @classmethod
    async def fetch_repo_comments(cls, ownername: str, reponame: str):
        url = f"https://api.github.com/repos/{ownername}/{reponame}/comments"
        return await cls._fetch(url)

    @classmethod
    async def fetch_repo_commits(cls, ownername: str, reponame: str):
        url = f"https://api.github.com/repos/{ownername}/{reponame}/commits"
        return await cls._fetch(url)


class CachedGithubManager(GithubManager):
    """
    Extends base Request class to cache api responses
    """

    cache = RedisBackend(expire_after=60 * 60)  # 3600 seconds

    @classmethod
    async def _fetch(cls, url: str):
        async with CachedSession(cache=cls.cache, headers=cls.headers) as session:
            async with session.get(url) as res:
                
                if res.status == 400:
                    raise BadRequest()
                elif res.status == 404:
                    raise NotFound()

                result = await res.json()
                logger.info(
                    f"URL:{url} - Cached:{res.from_cache} - Created at:{res.created_at} - Expires in:{res.expires} - Is expired:{res.is_expired}"
                )
                return result

