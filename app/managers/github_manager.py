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

        
class GithubManager(RequestManager):

    def __init__(self, timeout_total: int = None) -> None:
        # get persistent cached session
        self._app = Sanic.get_app()
        _session = self._app.ctx.cached_session
        # github creds
        _token = os.getenv("GITHUB_PAT")
        # set headers
        _headers = {
            "Accept":  "application/vnd.github+json",
            "Authorization": f"Bearer {_token}",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        super().__init__(session=_session, headers=_headers, timeout_total=timeout_total)

class AuthenticatedGithubManager(RequestManager):
    
    def __init__(self, timeout_total: int = None) -> None:
        # get persistent cached session
        self._app = Sanic.get_app()
        _session = self._app.ctx.client_session
        # github creds
        _token = os.getenv("GITHUB_PAT_2")
        # set headers
        _headers = {
            "Accept":  "application/vnd.github+json",
            "Authorization": f"Bearer {_token}",
            "X-GitHub-Api-Version": "2022-11-28"
        }
        super().__init__(session=_session, headers=_headers, timeout_total=timeout_total)