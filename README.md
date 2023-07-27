# (MINI) Github Analytics Project

Setup for local dev:

Build
```sh
py -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

<details>
<summary>Redis Installation</summary>
GOSH! You seriously opened it 
</details>

Run
```sh
# start redis server
$ redis-server

# check if redis is up and on proper address
$ redis-cli
host:port> ping
PONG

# start sanic server
sanic app.server --dev
```

Now go to,
localhost:8000/docs to get info on various available routes


<details>
<summary>Local Demos</summary>
OpenAPI Swagger
http://127.0.0.1:8000/docs/


### User demo

Google | Github
http://127.0.0.1:8000/user/google

Twitter | Github
http://127.0.0.1:8000/user/twitter

Miguel Grinberg | Github
http://localhost:8000/user/miguelgrinberg

Andrej | Github
http://localhost:8000/user/karpathy

#### Compare

Compare User
http://127.0.0.1:8000/user/compare?user1=google&user2=twitter

Compare User
http://127.0.0.1:8000/user/compare?user1=miguelgrinberg&user2=karpathy

### Repo demo

google/leveldb | Github
http://127.0.0.1:8000/repo/google/leveldb

pallets/flask | Github
http://localhost:8000/repo/pallets/flask

sanic-org/sanic | Github
http://localhost:8000/repo/sanic-org/sanic

aio-libs/aiohttp | Github
http://localhost:8000/repo/aio-libs/aiohttp

#### Compare

google/leveldb vs facebook/rocksdb
http://localhost:8000/repo/compare?user1=google&repo1=leveldb&user2=facebook&repo2=rocksdb

sanic-org/sanic vs pallets/flask
http://localhost:8000/repo/compare?user1=sanic-org&repo1=sanic&user2=pallets&repo2=flask


</details>



## Links 

How to retrieve contribution graph data from the GitHub API | by Yuichi Yogo | Medium
https://medium.com/@yuichkun/how-to-retrieve-contribution-graph-data-from-the-github-api-dc3a151b4af

## TODO 
- [x] Logging
- [x] Refactoring to OOP
- [ ] Tests