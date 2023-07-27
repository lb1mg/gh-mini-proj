from pydantic import BaseModel
from typing import Optional


class Repo(BaseModel):
    full_name:str
    description:str
    license:Optional[dict]
    language:Optional[str]
    forks:int
    open_issues:int
    watchers:int
    subscribers_count:int
    network_count:int
    owner:Optional[dict]

class Contributors(BaseModel):
    avatar_url:str
    login:str
    contributions:int

class Stargazers(BaseModel):
    avatar_url:str
    login:str

class Comments(BaseModel):
    pass

class Commits(BaseModel):
    commiter:dict
    commit:dict
    parents:list