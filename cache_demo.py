from dotenv import load_dotenv
load_dotenv()
import time
import asyncio

from app.managers.myrequest import CachedRequest

if __name__ == '__main__':
    DEMO_USER = 'miguelgrinberg'
    s = time.perf_counter()
    result = asyncio.run(CachedRequest.fetch_user_repos(DEMO_USER))
    print(f'Time taken: {time.perf_counter()-s}')