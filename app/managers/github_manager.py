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

from app.managers.request_manager import RequestManager

        
class GithubManager:

    def __init__(self, cache:bool=True, timeout_total:int=180) -> None:
        # github creds
        _token = os.getenv("GITHUB_PAT_2")
        # set headers
        _headers = {
            "Accept":  "application/vnd.github+json",
            "Authorization": f"Bearer {_token}",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        self.req_manager = RequestManager(cache=cache, headers=_headers, timeout_total=timeout_total)
        