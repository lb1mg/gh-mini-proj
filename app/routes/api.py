"""
WIP
"""
from sanic import Blueprint, Request
from sanic.response import redirect, text, json
from sanic_ext import render

api_bp = Blueprint('apibp', url_prefix='/api')

@api_bp.get('/repo')
def get_repo(request):
    pass

@api_bp.post('/repo')
def create_repo(request):
    pass

@api_bp.route('/repo', methods=['UPDATE'])
def update_repo(request):
    pass

@api_bp.route('/repo', methods=['DELETE'])
def delete_repo(request):
    pass