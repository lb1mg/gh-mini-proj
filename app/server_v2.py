import os
from dotenv import load_dotenv
load_dotenv()

import sentry_sdk
from sentry_sdk.integrations.sanic import SanicIntegration

from sanic import Sanic

# Blueprints
from app.routes.main import main_bp
from app.routes.users import users_bp
from app.routes.repos import repos_bp

# Listeners
from app.listeners import connect_redis, disconnect_redis

# Middlewares
from app.middlewares import add_request_id_header, add_security_headers

# Exceptions
from redis import ConnectionError
from pydantic import ValidationError
from app.exceptions import redis_conn_err_handler, pydantic_val_err_handler

def setup_sentry():
    sentry_sdk.init(
    dsn= os.getenv('SENTRY_DSN'),
    integrations=[
        SanicIntegration(),        
    ],
    traces_sample_rate=1.0,
    )


def add_blueprints(app:Sanic):
    app.blueprint(main_bp)
    app.blueprint(users_bp)
    app.blueprint(repos_bp)
    return app

def register_listeners(app:Sanic):
    app.register_listener(connect_redis, 'before_server_start')
    app.register_listener(disconnect_redis, 'before_server_stop')
    return app

def register_middlewares(app:Sanic):
    app.register_middleware(add_request_id_header, "response")
    app.register_middleware(add_security_headers, "response")
    return app

def add_error_handlers(app:Sanic):
    app.error_handler.add(ConnectionError, redis_conn_err_handler)
    app.error_handler.add(ValidationError, pydantic_val_err_handler)
    return app


# App factory
def create_app():
    # Setup Sentry SDK
    setup_sentry()
    # Instantiate Sanic app
    app = Sanic('mini-gh-analytics')
    # TODO: Configuration
    app.config.FALLBACK_ERROR_FORMAT = "json"
    # Sanic Extention Config
    app.extend(config={"oas_ui_default": "swagger"})
    # Registering Blueprints
    app = add_blueprints(app)
    # Registering Listeners
    app = register_listeners(app)
    # Registering Middlewares
    app = register_listeners(app)
    # Registering custom Error Handlers
    app = add_error_handlers(app)
    return app