from pydantic import BaseModel
from typing import Optional

class User(BaseModel):
    login: str
    avatar_url: str
    html_url: str
    type: str
    site_admin: bool
    name: Optional[str]
    blog: Optional[str]
    location: Optional[str]
    email: Optional[str]
    bio: Optional[str]
    twitter_username: Optional[str]
    public_repos: int
    public_gists: int
    followers: int
    following: int
    created_at: str
    updated_at: str

class UserRepo(BaseModel):
    full_name: str
    html_url: str
    description: Optional[str]
    url: str
    archive_url: str
    forks_count:int
    open_issues_count:int
    watchers_count:int
    license:Optional[dict]

class Follower(BaseModel):
    avatar_url:str
    login:str

class Event(BaseModel):
    type:str
    repo:dict
    created_at:str