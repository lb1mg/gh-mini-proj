from pprint import pprint
import asyncio

import time

from sanic import Blueprint
from sanic import response
from sanic.exceptions import NotFound, BadRequest
from sanic_ext import render

from app.managers.user_manager import UserManager

users_bp = Blueprint('users_bp', url_prefix='/user')


@users_bp.get('/<username:str>')
async def get_user_info(request, username:str):
    args = request.args
    sort_arg = args.get('sort')
    order_arg = args.get('order')
    
    user_info, user_repos, user_events, user_followers = await UserManager().fetch_user(username)
    
    """ sorting repos """
    reverse = True
    sort_msg = None
    if sort_arg:
        if order_arg and order_arg=='asc':
            reverse=False            
        if sort_arg=='forks':
            user_repos.sort(key=lambda x:x.forks_count, reverse=reverse)
            sort_msg = f'sorted by forks count'
        elif sort_arg=='stars':
            user_repos.sort(key=lambda x:x.watchers_count, reverse=reverse)
            sort_msg = f'sorted by stars count'
    
    return await render('user.html', context={
        'user_info':user_info, 
        'user_repos':user_repos, 
        'user_events':user_events, 
        'user_followers':user_followers,
        'sort_msg': sort_msg
    })


@users_bp.get('/compare')
async def compare(request):
    args = request.args
    user1 = args.get('user1')
    user2 = args.get('user2')
    
    if not user1 or not user2:
        raise BadRequest('Missing arguements!')
    
    user1_info, user2_info = await UserManager().compare_user(user1, user2)
    
    return await render('compare_user.html', context={
        'user1_info':user1_info,
        'user2_info':user2_info
    })