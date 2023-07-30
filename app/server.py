import os
from dotenv import load_dotenv
load_dotenv()

from sanic import Sanic

# Blueprints
from app.routes.main import main_bp
from app.routes.users import users_bp
from app.routes.repos import repos_bp

# Listeners
from app.listeners import connect_redis, disconnect_redis

# Middlewares
from app.middlewares import add_request_id_header, add_security_headers



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
    app.register_listener(connect_redis, 'before_server_start')
    app.register_listener(disconnect_redis, 'before_server_stop')
    
    # Registering Middlewares
    app.register_middleware(add_request_id_header, "response")
    app.register_middleware(add_security_headers, "response")
    
    return app