from pprint import pprint

from sanic import Blueprint
from sanic import response
from sanic.exceptions import NotFound, BadRequest
from sanic_ext import render

from managers.myrequest import Request, CachedRequest

repos_bp = Blueprint('repos_bp', url_prefix='/repo')

@repos_bp.get('/<ownername:str>/<reponame:str>')
async def get_repo_info(request, ownername:str, reponame:str):
    repo_info = await CachedRequest.fetch_repo(ownername, reponame)
    return await render('repo.html', context={'repo_info':repo_info})
    