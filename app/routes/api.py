"""
WIP
"""
from sanic.log import logger
from sanic import Blueprint, Request
from sanic.response import redirect, text, json
from sanic_ext import render
from app.managers.repo_manager import PrivateRepoManager

api_bp = Blueprint('apibp', url_prefix='/api')

@api_bp.route('/repo', methods=['GET'])
async def get_repo(request:Request):
    raise NotImplementedError()

@api_bp.route('/repo', methods=['POST'])
async def create_repo(request):
    body = request.json
    from pprint import pprint
    pprint(body)
    repo_name = body.get('repo_name')
    description = body.get('description')
    private = body.get('private')
    is_template = body.get('is_template')
    res = await PrivateRepoManager().create_repo(
        repo_name=repo_name,
        description=description,
        private=private,
        is_template=is_template
    )
    logger.info(res)
    return json(
        {'msg':'repo created!'},
        status=200
    )

@api_bp.route('/repo', methods=['PUT'])
async def update_repo(request):
    raise NotImplementedError()

@api_bp.route('/repo', methods=['DELETE'])
async def delete_repo(request):
    body = request.json
    from pprint import pprint
    pprint(body)
    owner_name = body.get('owner_name')
    repo_name = body.get('repo_name')
    res = await PrivateRepoManager().delete_repo(
        owner_name=owner_name,
        repo_name=repo_name
    )
    logger.info(res)
    return json(
        {'msg':f'repo: {owner_name}/{repo_name} deleted!'},
        status=200
    )