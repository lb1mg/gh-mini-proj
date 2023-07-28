from sanic import Blueprint
from sanic.response import redirect
from sanic_ext import render

main_bp = Blueprint('mainbp')

@main_bp.get('/')
async def get_index(request):
    return redirect('/help')

@main_bp.get('/help')
async def get_help(request):
    return await render('help.html')