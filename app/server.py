import os
from dotenv import load_dotenv
load_dotenv()
# print(f"testing dotenv: {os.getenv('GITHUB_PAT')}")

from sanic import Sanic
from sanic.response import text, json, redirect
from sanic.exceptions import NotFound, BadRequest
from sanic_ext import render

# Blueprints
from routes.users import users_bp
from routes.orgs import orgs_bp
from routes.repos import repos_bp


app = Sanic(__name__)

# Sanic Extention Config
app.extend(config={"oas_ui_default": "swagger"})

# Registering Blueprints
app.blueprint(users_bp)
app.blueprint(orgs_bp)
app.blueprint(repos_bp)

@app.get('/')
async def get_index(request):
    return redirect('/help')

@app.get('/help')
async def get_help(request):
    return await render('help.html')
    
if __name__ == '__main__':
    app.run(port=8000, dev=True)