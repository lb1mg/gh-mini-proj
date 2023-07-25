from pprint import pprint
import asyncio

from sanic import Blueprint
from sanic import response
from sanic.exceptions import NotFound, BadRequest
from sanic_ext import render

from managers.myrequest import Request, CachedRequest

repos_bp = Blueprint('repos_bp', url_prefix='/repo')

@repos_bp.get('/<ownername:str>/<reponame:str>')
async def get_repo_info(request, ownername:str, reponame:str):
    # repo_info = await CachedRequest.fetch_repo(ownername, reponame)
    # repo_contributors = await CachedRequest.fetch_repo_contributors(ownername, reponame)
    # repo_stargazers  =await CachedRequest.fetch_repo_stargazers(ownername, reponame)
    # repo_comments = await CachedRequest.fetch_repo_comments(ownername, reponame)
    # repo_commits = await CachedRequest.fetch_repo_commits(ownername, reponame)
    
    repo_info, repo_contributors, repo_stargazers, repo_comments, repo_commits = await asyncio.gather(
        CachedRequest.fetch_repo(ownername, reponame),
        CachedRequest.fetch_repo_contributors(ownername, reponame),
        CachedRequest.fetch_repo_stargazers(ownername, reponame),
        CachedRequest.fetch_repo_comments(ownername, reponame),
        CachedRequest.fetch_repo_commits(ownername, reponame)
    )
    
    # print(repo_collaborators)
    return await render('repo.html', context={'repo_info':repo_info, 'repo_contributors':repo_contributors, 'repo_stargazers':repo_stargazers, 'repo_comments':repo_comments, 'repo_commits':repo_commits})    

@repos_bp.get('/compare')
async def compare(request):
    args = request.args
    # print(args)
    user1 = args.get('user1')
    repo1 = args.get('repo1')
    user2 = args.get('user2')
    repo2 = args.get('repo2')
    
    if (not user1 or not user2 or not repo1 or not repo2):
        raise BadRequest()
    
    # user1_info = await CachedRequest.fetch_user(user1)
    # user2_info = await CachedRequest.fetch_user(user2)
    
    repo1_info, repo2_info = await asyncio.gather(
        CachedRequest.fetch_repo(user1, repo1),
        CachedRequest.fetch_repo(user2, repo2)
    )
    return await render('compare_repo.html', context={
        'repo1_info':repo1_info,
        'repo2_info':repo2_info
    })