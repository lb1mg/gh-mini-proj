import asyncio
from app.managers.myrequest import Request

if __name__ == '__main__':
    asyncio.run(Request.fetch_user('google'))