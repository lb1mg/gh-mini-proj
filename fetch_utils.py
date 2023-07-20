from pprint import pprint

import aiohttp
import asyncio
                        

async def fetch(url:str):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as res:
            # log status here
            return await res.json()

async def fetch_user(username:str):
    url = f'https://api.github.com/users/{username}'
    return await fetch(url)
    
            
async def fetch_user_repos(username:str):
    url = f'https://api.github.com/users/{username}/repos'
    return await fetch(url)

async def fetch_repo(ownername:str, reponame:str):
    url = f'https://api.github.com/repos/{ownername}/{reponame}'
    return await fetch(url)

async def fetch_org(orgname:str):
    url = f'https://api.github.com/orgs/{orgname}'
    return await fetch(url)

async def fetch_org_repos(orgname:str):
    url = f'https://api.github.com/orgs/{orgname}/repos'
    return await fetch(url)



if __name__ == '__main__':
    result = asyncio.run(fetch_user('miguelgrinberg'))
    # result = asyncio.run(fetch_user_repos('miguelgrinberg'))
    # result = asyncio.run(fetch_repo('miguelgrinberg', 'microblog'))
    result = asyncio.run(fetch_repo('google', 'leveldb'))
    # result = asyncio.run(fetch_org('google'))
    # result = asyncio.run(fetch_org_repos('google'))
    # print(type(result))
    pprint(result)