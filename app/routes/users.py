from pprint import pprint
import asyncio

import time

from sanic import Blueprint
from sanic import response
from sanic.exceptions import NotFound, BadRequest
from sanic_ext import render

from app.managers.myrequest import Request, CachedRequest

users_bp = Blueprint('users_bp', url_prefix='/user')


@users_bp.get('/<username:str>')
async def get_user_info(request, username:str):

    # user_info = await CachedRequest.fetch_user(username)
    # user_repos = await CachedRequest.fetch_user_repos(username)
    # user_events = await CachedRequest.fetch_user_events(username)
    # user_followers = await CachedRequest.fetch_user_followers(username)
    
    s = time.perf_counter()
    user_info, user_repos, user_events, user_followers = await asyncio.gather(
        CachedRequest.fetch_user(username),
        CachedRequest.fetch_user_repos(username),
        CachedRequest.fetch_user_events(username),
        CachedRequest.fetch_user_followers(username)
    )
    print(f'Elapsed Time {time.perf_counter()-s}s')
    # print(user_info)
    # print(user_repos)
    return await render('user.html', context={'user_info':user_info, 'user_repos':user_repos, 'user_events':user_events, 'user_followers':user_followers})


@users_bp.get('/compare')
async def compare(request):
    args = request.args
    # print(args)
    user1 = args.get('user1')
    user2 = args.get('user2')
    if not user1 or not user2:
        raise BadRequest()
    
    # user1_info = await CachedRequest.fetch_user(user1)
    # user2_info = await CachedRequest.fetch_user(user2)
    
    user1_info, user2_info = await asyncio.gather(
        CachedRequest.fetch_user(user1),
        CachedRequest.fetch_user(user2)
    )
    return await render('compare_user.html', context={
        'user1_info':user1_info,
        'user2_info':user2_info
    })
        