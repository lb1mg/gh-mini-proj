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
    repo_contributors = await CachedRequest.fetch_repo_contributors(ownername, reponame)
    repo_stargazers  =await CachedRequest.fetch_repo_stargazers(ownername, reponame)
    repo_comments = await CachedRequest.fetch_repo_comments(ownername, reponame)
    repo_commits = await CachedRequest.fetch_repo_commits(ownername, reponame)
    # print(repo_collaborators)
    return await render('repo.html', context={'repo_info':repo_info, 'repo_contributors':repo_contributors, 'repo_stargazers':repo_stargazers, 'repo_comments':repo_comments, 'repo_commits':repo_commits})    