from pprint import pprint

from sanic import Blueprint
from sanic import response
from sanic.exceptions import NotFound, BadRequest
from sanic_ext import render

from managers.myrequest import Request, CachedRequest

orgs_bp = Blueprint('orgs_bp', url_prefix='/org')