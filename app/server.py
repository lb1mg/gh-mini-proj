import os
from dotenv import load_dotenv
load_dotenv()
from typing import List

import aiohttp
from aiohttp_client_cache import CachedSession

from sanic import Sanic

# Blueprints
from app.routes.main import main_bp
from app.routes.users import users_bp
from app.routes.repos import repos_bp
from app.routes.api import api_bp

# Listeners
from app.listeners import BaseListener, RedisListener, ClientSessionListener, CachedSessionListener

# Middlewares
from app.middlewares import add_request_id_header, add_security_headers

# Exceptions
import redis
import pydantic
from app.exceptions import redis_conn_err_handler, pydantic_val_err_handler

# sentry
import sentry_sdk
from sentry_sdk.integrations.sanic import SanicIntegration

def setup_sentry():
    sentry_sdk.init(
        dsn= os.getenv('SENTRY_DSN'),
        integrations=[
            SanicIntegration(),        
        ],
        traces_sample_rate=1.0,
    )

def register_listener(app:Sanic, listener:BaseListener):
    app.register_listener(listener.connect, 'before_server_start')
    app.register_listener(listener.disconnect, 'before_server_stop')

def register_listeners(app:Sanic, listeners:List[BaseListener]):
    for listener in listeners:
        register_listener(app, listener)

# App factory
def create_app():
    
    setup_sentry()
    
    app = Sanic('mini-gh-analytics')

    # TODO: Configuration
    app.config.FALLBACK_ERROR_FORMAT = "json"
    
    # Sanic Extention Config
    app.extend(config={"oas_ui_default": "swagger"})

    # Registering Blueprints
    app.blueprint(main_bp)
    app.blueprint(users_bp)
    app.blueprint(repos_bp)
    app.blueprint(api_bp)
    
    # Registering Listeners
    listeners = [RedisListener, ClientSessionListener, CachedSessionListener]
    register_listeners(app, listeners)
    
    # Registering Middlewares
    app.register_middleware(add_request_id_header, "response")
    app.register_middleware(add_security_headers, "response")
    
    # Registering custom Error Handlers
    app.error_handler.add(redis.ConnectionError, redis_conn_err_handler)
    app.error_handler.add(pydantic.ValidationError, pydantic_val_err_handler)
    # TODO: aiohttp.ClientConnectorError
    
    return app