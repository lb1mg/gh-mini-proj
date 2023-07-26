from dotenv import load_dotenv
load_dotenv()
import time
from pprint import pprint
import asyncio

from app.managers.github_manager import GithubManager, CachedGithubManager
from app.models.users import User, UserRepo

if __name__ == '__main__':
    # result = asyncio.run(CachedRequest.fetch_user('miguelgrinberg'))
    # user = User(**result)
    # print(user['name'])
    
    result = asyncio.run(CachedGithubManager.fetch_user_repos('miguelgrinberg'))
    # user_repos = [UserRepo(**repo) for repo in result]
    user_repos = result
    # pprint(user_repos)
    for repo in user_repos:
        print(repo.forks_count, end=', ')
    print()    
    
    
    user_repos.sort(key=lambda x:x.forks_count, reverse=True)
    
    for repo in user_repos:
        print(repo.forks_count, end=', ')
    # result = asyncio.run(fetch_repo('miguelgrinberg', 'microblog'))
    # result = asyncio.run(fetch_repo('google', 'leveldb'))
    # result = asyncio.run(CachedRequest.fetch_org('bloomberg'))
    # result = asyncio.run(CachedRequest.fetch_user('livewire'))
    # result = asyncio.run(Request.fetch_org('google'))
    # result = asyncio.run(fetch_org_repos('google'))
    # result = asyncio.run(Request.fetch_user('llllllllllllllll'))
    # result = asyncio.run(CachedRequest.fetch_org('facebookresearch'))
    # asyncio.run(CachedRequest._get_cached_urls())
    # print(type(result))
    # pprint(result)
    pass