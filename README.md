# Github Analytics Project

Instructions to run:
```
py -m venv venv
source venv/bin/activate
cd app
python server.py
```

Now go to,
localhost:8000/docs to get info on various available routes

## For Demo

OpenAPI Swagger
http://127.0.0.1:8000/docs/

Google | Github
http://127.0.0.1:8000/user/google

Twitter | Github
http://127.0.0.1:8000/user/twitter

Compare User
http://127.0.0.1:8000/user/compare?user1=google&user2=twitter

REPO NAME | Github
http://127.0.0.1:8000/repo/google/leveldb


----

How to retrieve contribution graph data from the GitHub API | by Yuichi Yogo | Medium
https://medium.com/@yuichkun/how-to-retrieve-contribution-graph-data-from-the-github-api-dc3a151b4af

## TODO 
- [ ] Logging
- [ ] Refactoring to OOP
- [ ] Tests