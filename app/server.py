import os
from dotenv import load_dotenv
load_dotenv()

from sanic import Sanic
from sanic import Request

# Blueprints
from app.routes.main import main_bp
from app.routes.users import users_bp
from app.routes.repos import repos_bp

# Middlewares
from app.middlewares import add_request_id_header

# App factory
def create_app():
    app = Sanic('mini-gh-analytics')

    # Sanic Extention Config
    app.extend(config={"oas_ui_default": "swagger"})

    # Registering Blueprints
    app.blueprint(main_bp)
    app.blueprint(users_bp)
    app.blueprint(repos_bp)
    
    # Registering Listeners
    
    
    # Registering Middlewares
    app.register_middleware(add_request_id_header, "response")
    
    return app