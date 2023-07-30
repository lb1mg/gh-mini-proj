from sanic import Blueprint, Request
from sanic.response import redirect, text, json
from sanic_ext import render

main_bp = Blueprint('mainbp')

@main_bp.get('/')
async def get_index(request):
    return redirect('/help')

@main_bp.get('/help')
async def get_help(request):
    return await render('help.html')

@main_bp.get('/ping')
async def ping(request):
    return json({'ping':'pong'})

@main_bp.get('/redis')
async def ping_redis(request):
    _redis = request.app.ctx.redis
    _pong = await _redis.ping()
    if not _pong:
        return json({'msg': 'not connected to redis!'})
    return json({'ping':'pong'})