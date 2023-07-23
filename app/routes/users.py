from pprint import pprint

from sanic import Blueprint
from sanic import response
from sanic.exceptions import NotFound, BadRequest
from sanic_ext import render

from managers.myrequest import Request, CachedRequest

users_bp = Blueprint('users_bp', url_prefix='/user')


@users_bp.get('/<username:str>')
async def get_user_info(request, username:str):
    user_info = await CachedRequest.fetch_user(username)
    user_repos = await CachedRequest.fetch_user_repos(username)
    return await render('user.html', context={'user_info':user_info, 'user_repos':user_repos})


@users_bp.get('/compare')
async def compare(request):
    args = request.args
    print(args)
    user1 = args.get('user1')
    user2 = args.get('user2')
    if user1 and user2:
        user1_info = await CachedRequest.fetch_user(user1)
        user2_info = await CachedRequest.fetch_user(user2)
        return await render('compare_user.html', context={
            'user1':user1_info,
            'user2':user2_info
        })
    else:
        raise BadRequest()