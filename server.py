from sanic import Sanic
from sanic.response import text, json, redirect
from sanic_ext import render

app = Sanic(__name__)

@app.route('/')
async def get_index(request):
    return redirect('/help')

@app.route('/help')
async def get_help(request):
    return await render('help.html')