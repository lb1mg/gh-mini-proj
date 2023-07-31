import os
from pprint import pprint
from typing import List, Tuple
import json

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

class RepoManager(GithubManager):
    
    def __init__(self, cache: bool = True, timeout_total: int = 180) -> None:
        super().__init__(cache, timeout_total)
        
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
        result =  await self.req_manager._fetch(url)
        repo = Repo(**result)
        return repo

    async def fetch_repo_contributors(self, ownername: str, reponame: str):
        url = f"https://api.github.com/repos/{ownername}/{reponame}/contributors"
        result =  await self.req_manager._fetch(url)
        contributors = [Contributors(**contributor) for contributor in result]
        return contributors

    async def fetch_repo_stargazers(self, ownername: str, reponame: str):
        url = f"https://api.github.com/repos/{ownername}/{reponame}/stargazers"
        return await self.req_manager._fetch(url)

    async def fetch_repo_comments(self, ownername: str, reponame: str):
        url = f"https://api.github.com/repos/{ownername}/{reponame}/comments"
        return await self.req_manager._fetch(url)

    async def fetch_repo_commits(self, ownername: str, reponame: str):
        url = f"https://api.github.com/repos/{ownername}/{reponame}/commits"
        return await self.req_manager._fetch(url)



class PrivateRepoManager(GithubManager):
    
    def __init__(self, cache: bool = False, timeout_total:int = 180) -> None:
        super().__init__(cache, timeout_total)
    
    def _raise_for_status(self, status: int) -> None:
        # TODO
        return super()._raise_for_status(status)
    
    async def create_repo(self, repo_name:str, description:str, private:bool, is_template:bool):
        payload = {
            'name':repo_name,
            'description':description,
            'private':private,
            'is_template':is_template
        }
        payload = json.dumps(payload)
        result = await self.req_manager._make_post(
            url='https://api.github.com/user/repos',
            payload=payload
        )
        return result
    
    async def get_repo(self):
        """ gets private repo """
        raise NotImplementedError()
    
    async def delete_repo(self, owner_name:str, repo_name:str):
        _url = f'  https://api.github.com/repos/{owner_name}/{repo_name}'
        result = await self.req_manager._make_delete(
            url=_url
        )
        return result
    
    async def update_repo(self):
        raise NotImplementedError