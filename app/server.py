import os
from dotenv import load_dotenv
load_dotenv()

from sanic import Sanic
from sanic.response import text, json, redirect
from sanic.exceptions import NotFound, BadRequest
from sanic_ext import render

# Blueprints
from app.routes.users import users_bp
from app.routes.repos import repos_bp

app = Sanic('mini-gh-analytics')

# Sanic Extention Config
app.extend(config={"oas_ui_default": "swagger"})

# Registering Blueprints
app.blueprint(users_bp)
app.blueprint(repos_bp)

@app.get('/')
async def get_index(request):
    return redirect('/help')

@app.get('/help')
async def get_help(request):
    return await render('help.html')
    
# if __name__ == '__main__':
#     app.run(port=8000, dev=True)
    # app.run()