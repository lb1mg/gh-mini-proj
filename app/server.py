import os
from dotenv import load_dotenv
load_dotenv()

from sanic import Sanic
from sanic.response import text, json, redirect
from sanic.exceptions import NotFound, BadRequest
from sanic_ext import render

# Blueprints
from app.routes.main import main_bp
from app.routes.users import users_bp
from app.routes.repos import repos_bp

def create_app():
    app = Sanic('mini-gh-analytics')

    # Sanic Extention Config
    app.extend(config={"oas_ui_default": "swagger"})

    # Registering Blueprints
    app.blueprint(main_bp)
    app.blueprint(users_bp)
    app.blueprint(repos_bp)
    
    return app



    
# if __name__ == '__main__':
#     app.run(port=8000, dev=True)
    # app.run()